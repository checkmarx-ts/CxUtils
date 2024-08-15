""" 
========================================================================

SIMPLE CLASS FOR CXSAST REST API CALLS
Supports v9.0 and up

joao.costa@checkmarx.com
PS-EMEA
10-11-2022

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

BREATH_CALLS: int   = 100
BREATH_SLEEP: float = 1.0

class sastapi(object):

    def __init__(self):
        self.__token        = None
        self.__callcounter  = 0
        self.__retry        = 3
        self.__host         = None
        self.__uname        = None
        self.__pword        = None
        self.__scope        = None
        self.__client       = None
        self.__proxyhost    = None

    def __init__(self, fqdn, username, password, scope, client, proxy_url = None, proxy_username = None, proxy_password = None ) :
        self.__token        = None
        self.__callcounter  = 0
        self.__retry        = 3
        self.__host         = fqdn.strip().lower().rstrip('/')
        self.__uname        = username
        self.__pword        = password
        self.__scope        = scope
        self.__client       = client
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


    def get_auth_token(self):
        sapipath = self.__host + '/cxrestapi/auth/identity/connect/token'
        shead   = { 'Content-Type':'application/x-www-form-urlencoded' }
        sbody   = { 'username':self.__uname,
                    'password':self.__pword,
                    'grant_type':'password',
                    'scope':self.__scope,
                    'client_id':self.__client,
                    'client_secret':'014DF517-39D1-4453-B7B3-9930C563627C'
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
        sodata: bool    = False
        smessage: str   = None

        # Resolve path
        sapipath = self.__host + uri
        if not ( '%' in uri or '?' in uri or '&' in uri ) :
            sapipath = sapipath.lower()

        # Check ODATA
        sodata = 'cxwebinterface/odata/' in sapipath.lower()
        if sodata and verb != 'get' :
            raise Exception( 'Only get verb is allowed from ODATA')
        
        # Resolve body contents - if body exists and is not string
        if body and ((type(body) is dict) or (type(body) is list)) :
            sbody = json.dumps(body)
        else :
            sbody = body

        # Resolve api version
        if apiversion :
            version = apiversion 
        else :
            version = '1.0'

        # Breath a moment
        self.__callcounter += 1
        if self.__callcounter > BREATH_CALLS :
            time.sleep(BREATH_SLEEP)
            self.__callcounter = 0

        # Ensure we are authenticated
        if (self.__token == '') or (self.__token is None) :
            self.get_auth_token()

        # Go for it
        while (scounter <= self.__retry) :
            scounter += 1
            sresponse = None
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST API recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST API recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            # Compose header
            shead = {
                        "Authorization":self.__token,
                        "Cache-Control": "no-cache",
                        "Accept": "application/json",
                        "Content-Type": "application/json;v=" + version
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
                cxlogger.logdebug( 'SAST API error, verb "' + verb + '", path "' + sapipath + '"', e )
                if scounter > self.__retry :
                    raise e
                else :
                    sloop = True
                
            # Check result
            if (sresponse != None) :
                # Return the result (may be odata)
                if sresponse.status_code in [OK, MULTI_STATUS, CREATED, NO_CONTENT, ACCEPTED] :
                    if sresponse.content and len(sresponse.content) > 3:
                        if (sodata) :
                            try:
                                sret = sresponse.json()
                                return sret['value']
                            except:
                                try :
                                    sret = sresponse.text
                                    if sret.startswith('ï»¿') :
                                        sret = sret[3:]
                                    return sret
                                except :
                                    return []
                        else :
                            return sresponse.json()
                    else :
                        return []
                # Token expired. Give it 2, 4, 8 seconds and get a new one
                elif sresponse.status_code == UNAUTHORIZED :
                    smessage = str(sresponse.status_code) + ' ' + sresponse.text
                    time.sleep( scounter * 2 )
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
                # Connection lost. Give it 5, 10, 15 seconds and reconnect
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
        return self.__internal_execute( 'get', uri, body, apiversion, headers )


    def put(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'put', uri, body, apiversion, headers )


    def post(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'post', uri, body, apiversion, headers )


    def patch(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'patch', uri, body, apiversion, headers )


    def delete(self, uri, body = None, apiversion = None, headers = None) :
        return self.__internal_execute( 'delete', uri, body, apiversion, headers )
