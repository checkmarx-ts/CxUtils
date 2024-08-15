""" 
========================================================================

SIMPLE CLASS FOR CXONE REST API CALLS

joao.costa@checkmarx.com
PS-EMEA
22-12-2022

========================================================================
"""

import time
import json
import requests
import http
from urllib import parse
from urllib3.exceptions import InsecureRequestWarning
from urllib3 import disable_warnings
from cxloghandler import cxlogger

# Disable certificate exception (for self-signed)
disable_warnings(category=InsecureRequestWarning)

OK                  = http.HTTPStatus.OK
MULTI_STATUS        = http.HTTPStatus.MULTI_STATUS
BAD_REQUEST         = http.HTTPStatus.BAD_REQUEST
NOT_FOUND           = http.HTTPStatus.NOT_FOUND
UNAUTHORIZED        = http.HTTPStatus.UNAUTHORIZED
CREATED             = http.HTTPStatus.CREATED
FORBIDDEN           = http.HTTPStatus.FORBIDDEN
NO_CONTENT          = http.HTTPStatus.NO_CONTENT
ACCEPTED            = http.HTTPStatus.ACCEPTED
CONFLICT            = http.HTTPStatus.CONFLICT
BAD_GATEWAY         = http.HTTPStatus.BAD_GATEWAY
SERVICE_UNAVAILABLE = http.HTTPStatus.SERVICE_UNAVAILABLE
GATEWAY_TIMEOUT     = http.HTTPStatus.GATEWAY_TIMEOUT

BREATH_CALLS: int   = 50
BREATH_SLEEP: float = 1.0            


class cxoneapi(object):

    def __init__(self):
        self.__accessctrl   = False
        self.__callcounter  = 0
        self.__token        = None
        self.__retry        = 3
        self.__tenant       = None
        self.__host         = None
        self.__keycloak     = None
        self.__apikey       = None
        self.__clientid     = None
        self.__granttype    = None
        self.__proxyhost    = None


    def __init__(self, fqdn, tenant, apikey, aclfqdn = None, clientid = None, granttype = None, proxy_url = None, proxy_username = None, proxy_password = None, access_control = False ) :
        self.__accessctrl   = access_control    
        self.__callcounter  = 0
        self.__token        = None
        self.__retry        = 3
        self.__tenant       = tenant
        self.__host         = fqdn.strip().lower().rstrip('/')
        # Resolve keycloak endpoint from fqdn, if it is not supplyed
        if not aclfqdn :
            if self.__host.startswith( 'https://ast' ) :
                self.__keycloak = 'https://iam.checkmarx.net'
            else :
                self.__keycloak = self.__host[0: self.__host.find('.')] + '.iam.checkmarx.net'
        else :
            self.__keycloak = aclfqdn.strip().lower().rstrip('/')
        self.__apikey       = apikey
        self.__clientid     = clientid
        if not self.__clientid :
            self.__clientid = 'ast-app'
        self.__granttype    = granttype
        if not self.__granttype :
            if self.__clientid == 'ast-app' :
                self.__granttype = 'refresh_token'
            else :
                self.__granttype = 'client_credentials'
        # Detect if using oauth or apikey
        if self.__clientid != 'ast-app' or self.__granttype != 'refresh_token' :
            self.__granttype    = 'client_credentials'
        # Check proxy
        self.__proxyhost    = None
        if proxy_url :
            proxyurl = proxy_url.lower()
            if proxy_username or proxy_password :
                proxyprotocol = ''
                proxyendpoint = proxyurl
                sep = proxyurl.find('://')
                if sep > 0 :
                    proxyprotocol = proxyurl[0:sep+3]
                    proxyendpoint = proxyurl[sep+3:]
                    proxyurl = proxyprotocol + parse.quote(proxy_username, safe = '') + ':' + parse.quote(proxy_password, safe = '') + '@' + proxyendpoint
            self.__proxyhost  = { 'http': proxyurl, 'https': proxyurl }


    @property
    def __baseroot(self) :
        if self.__accessctrl :
            return self.__keycloak + '/auth/admin/realms/' + self.__tenant
        else :
            return self.__host
        
    
    def token(self) :
        tokendata = self.__token
        if tokendata :
            tokendata = tokendata[7:]            
        if not tokendata :
            tokendata = None
        return tokendata


    def get_auth_token(self):
        sapipath = self.__keycloak + '/auth/realms/' + self.__tenant + '/protocol/openid-connect/token'
        shead   = { 'Content-Type':'application/x-www-form-urlencoded' }
        if self.__granttype == 'client_credentials' :
            sbody   = { 'grant_type':self.__granttype,
                        'client_id':self.__clientid,
                        'client_secret':self.__apikey,
                      }
        else :
            sbody   = { 'grant_type':self.__granttype,
                        'client_id':self.__clientid,
                        'refresh_token':self.__apikey,
                      }

        sresponse = requests.post( sapipath, data = sbody, headers = shead, proxies = self.__proxyhost, verify = False )

        if sresponse != None :
            if sresponse.status_code != OK :
                raise ValueError('Code: ' + str(sresponse.status_code) + ' ' + sresponse.text)
            sjson = sresponse.json()
            self.__token = sjson.get("token_type") + " " + sjson.get("access_token")
        else :
            self.__token = None
        return self.__token
    

    def __internal_execute( self, verb: str, uri, body = None, apiversion = None, headers = None) :
        scounter: int   = 0
        sloop: bool     = False
        sresponse       = None
        smessage: str   = None

        # Resolve path
        sapipath = self.__baseroot + uri
        if not ( '%' in uri or '?' in uri or '&' in uri ) :
            sapipath = sapipath.lower()

        # Resolve body contents - if body exists and is not string
        if body and ((type(body) is dict) or (type(body) is list)) :
            sbody = json.dumps(body)
        else :
            sbody = body

        # Resolve api version
        if apiversion :
            version = ';version=' + apiversion 
        else :
            version = ''    

        # Breath a moment
        self.__callcounter += 1
        if self.__callcounter > BREATH_CALLS :
            time.sleep(BREATH_SLEEP)
            self.__callcounter = 0

        # Ensure we are authenticated
        if (self.__token == "") or (self.__token is None) :
            self.get_auth_token()


        while (scounter <= self.__retry) :
            scounter += 1
            sresponse = None
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'CXONE API recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'CXONE API recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            # Compose header
            shead = {
                        "Authorization": self.__token,
                        "Cache-Control": "no-cache",
                        "Accept": "application/json",
                        "Content-Type": "application/json" + version
                    }
            if headers :
                shead.update(headers)

            try :
                if verb == 'put' :
                    sresponse = requests.put( sapipath, data = sbody, headers = shead, allow_redirects = False, proxies = self.__proxyhost, verify = False )
                elif verb == 'patch' :
                    sresponse = requests.patch( sapipath, data = sbody, headers = shead, allow_redirects = False, proxies = self.__proxyhost, verify = False )
                elif verb == 'post' :
                    sresponse = requests.post( sapipath, data = sbody, headers = shead, allow_redirects = False, proxies = self.__proxyhost, verify = False )
                elif verb == 'delete' :
                    sresponse = requests.delete( sapipath, data = sbody, headers = shead, allow_redirects = False, proxies = self.__proxyhost, verify = False )
                else :  # get
                    sresponse = requests.get( sapipath, data = sbody, headers = shead, allow_redirects = False, proxies = self.__proxyhost, verify = False )
                sloop = False
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'CXONE API error, verb "' + verb + '", path "' + sapipath + '"', e )
                if scounter > self.__retry :
                    raise e
                else :
                    sloop = True

            # Check result
            if (sresponse != None) :
                # Return the result
                if sresponse.status_code in [OK, MULTI_STATUS, CREATED, NO_CONTENT, ACCEPTED] :
                    if sresponse.content and len(sresponse.content) > 3:
                        return sresponse.json()
                    else :
                        return []
                # Token expired. Give it 2, 4, 8 seconds and get a new one
                elif sresponse.status_code == UNAUTHORIZED :
                    smessage = str(sresponse.status_code) + ' ' + sresponse.text
                    time.sleep(1)
                    self.get_auth_token()
                # Connection lost. Give it 5, 10, 15 seconds and reconnect
                elif sresponse.status_code in [BAD_GATEWAY, SERVICE_UNAVAILABLE, GATEWAY_TIMEOUT] or sloop :
                    smessage = str(sresponse.status_code) + ' ' + sresponse.text
                    time.sleep( scounter * 5 )
                    self.get_auth_token()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError('Code: ' + str(sresponse.status_code) + ' ' + sresponse.text)
            else :
                # Connection lost. Give it 5, 10, 30 seconds and reconnect
                if sloop :
                    smessage = 'connection lost'
                    time.sleep( scounter * 5 )
                    self.get_auth_token()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError('General connection error')
                
        # Final check
        if (sresponse == None) :
            raise ValueError('General connection error')
        elif not ( sresponse.status_code in [OK, MULTI_STATUS, CREATED, NO_CONTENT, ACCEPTED] ) :
            raise ValueError('Code: ' + str(sresponse.status_code) + ' ' + sresponse.text)

            
    def get(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'get', uri, body, apiversion, headers)


    def put(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'put', uri, body, apiversion, headers)

    def patch(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'patch', uri, body, apiversion, headers)


    def post(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'post', uri, body, apiversion, headers)

      
    def delete(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'delete', uri, body, apiversion, headers)
