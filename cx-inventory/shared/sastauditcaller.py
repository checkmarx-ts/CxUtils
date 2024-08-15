""" 
========================================================================

SIMPLE CLASS FOR AUDIT SOAP CALLS
Supports v9.0 and up

joao.costa@checkmarx.com
PS-EMEA
10-11-2022

========================================================================
"""

import time
import http
import requests
from requests import Session
from zeep import Client, Settings
from zeep.transports import Transport
from time import sleep
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


relative_web_interface_url = "/CxWebInterface/Audit/CxAuditWebService.asmx?wsdl"

class auditapi(object):

    def __init__(self):
        self.__token        = None
        self.__callcounter  = 0
        self.__retry        = 3
        self.__host         = None
        self.__uname        = None
        self.__pword        = None
        self.__scope        = None
        self.__client       = None
        self.__sessid       = "0"
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
        self.__sessid       = "0"
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
        if sresponse.status_code != OK :
            raise ValueError('Code: ' + str(sresponse.status_code) + ' ' + sresponse.text)
        sjson = sresponse.json()
        self.__token = sjson.get("token_type") + " " + sjson.get("access_token")
        return self.__token



    def get_client_and_factory(self, authenticate = True ) :

        shead = None

        # Breath a moment
        self.__callcounter += 1
        if self.__callcounter > BREATH_CALLS :
            time.sleep(BREATH_SLEEP)
            self.__callcounter = 0            

        if authenticate :
            if not self.__token :
                self.get_auth_token()
            shead = { "Authorization":self.__token }

        settings = Settings(strict=False, force_https=True, xml_huge_tree=True, extra_http_headers=shead)

        session = Session()
        session.verify = False
        if self.__proxyhost :
            session.proxies = self.__proxyhost        
        transport = Transport(session=session)
        client = Client(
            wsdl = self.__host + relative_web_interface_url,
            transport = transport,
            settings = settings
        )

        client.transport.session.verify = False
        
        if self.__proxyhost :
            client.transport.session.proxies = self.__proxyhost

        factory = client.type_factory("ns0")

        return client, factory
    


    def getlicensedetails(self) :

        def execute():
            client, factory     = self.get_client_and_factory()
            return client.service.GetLicenseDetails(sessionId=self.__sessid)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None

        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST AUDIT recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST AUDIT recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST AUDIT error, "GetLicenseDetails"', e )
                if scounter > self.__retry :
                    raise e
                else :
                    sloop = True
            if response != None :
                if response.IsSuccesfull:
                    break
                # Token expired. Give it 2, 4, 8 seconds and get a new one
                elif not response.IsSuccesfull and ('12563' in response.ErrorMessage or 'Invalid_Token' in response.ErrorMessage) :
                    smessage = 'unauthorized  ' + response.ErrorMessage
                    time.sleep( scounter * 2 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Connection lost. Give it 5, 10, 15 seconds and reconnect
                elif sloop :
                    smessage = 'connection lost ' + response.ErrorMessage if response.ErrorMessage else ''
                    time.sleep( scounter * 5 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError( response.ErrorMessage )
            else :
                # Connection lost. Give it 5, 10, 30 seconds and reconnect
                if sloop :
                    smessage = 'connection lost'
                    time.sleep( scounter * 5 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError('General connection error')                    
        
        return response.Data.IsLicensed



    def queryupload(self, querydata) :

        def execute():
            client, factory     = self.get_client_and_factory()
            query_data = factory.ArrayOfCxWSQueryGroup([
                factory.CxWSQueryGroup(
                    Name=qg["Name"],
                    Impacts=factory.ArrayOfInt([i for i in qg["Impacts"]] if qg["Impacts"] else qg["Impacts"]),
                    PackageId=qg["PackageId"],
                    Queries=factory.ArrayOfCxWSQuery([
                        factory.CxWSQuery(
                            Name=q["Name"],
                            QueryId=q["QueryId"],
                            Source=q["Source"],
                            Cwe=q["Cwe"],
                            IsExecutable=q["IsExecutable"],
                            IsEncrypted=q["IsEncrypted"],
                            Severity=q["Severity"],
                            PackageId=q["PackageId"],
                            Status=factory.QueryStatus(q["Status"]),
                            Type=factory.CxWSQueryType(q["Type"]),
                            Categories=factory.ArrayOfCxQueryCategory([
                                factory.CxQueryCategory(
                                    Id=c["Id"],
                                    CategoryName=c["CategoryName"],
                                    CategoryType=factory.CxCategoryType(
                                        Id=c["CategoryType"]["Id"],
                                        Name=c["CategoryType"]["Name"],
                                        Order=c["CategoryType"]["Order"]
                                        )
                                    ) for c in q["Categories"]
                                ] if q["Categories"] else q["Categories"]),
                            CxDescriptionID=q["CxDescriptionID"],
                            QueryVersionCode=q["QueryVersionCode"],
                            EngineMetadata=q["EngineMetadata"]
                            ) for q in qg["Queries"]
                        ] if qg["Queries"] else qg["Queries"]),
                    IsReadOnly=qg["IsReadOnly"],
                    IsEncrypted=qg["IsEncrypted"],
                    Description=qg["Description"],
                    Language=qg["Language"],
                    LanguageName=qg["LanguageName"],
                    PackageTypeName=qg["PackageTypeName"],
                    ProjectId=qg["ProjectId"],
                    PackageType=factory.CxWSPackageTypeEnum(qg["PackageType"]),
                    PackageFullName=qg["PackageFullName"],
                    OwningTeam=qg["OwningTeam"],
                    Status=factory.QueryStatus(qg["Status"]),
                    LanguageStateDate=qg["LanguageStateDate"]
                    ) for qg in querydata
                ])
            return client.service.UploadQueries(sessionId=self.__sessid, queries=query_data)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None

        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST AUDIT recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST AUDIT recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST AUDIT error, "UploadQueries"', e )
                if scounter > self.__retry :
                    raise e
                else :
                    sloop = True
            if response != None :
                if response.IsSuccesfull:
                    break
                # Token expired. Give it 2, 4, 8 seconds and get a new one
                elif not response.IsSuccesfull and ('12563' in response.ErrorMessage or 'Invalid_Token' in response.ErrorMessage) :
                    smessage = 'unauthorized  ' + response.ErrorMessage
                    time.sleep( scounter * 2 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Connection lost. Give it 5, 10, 15 seconds and reconnect
                elif sloop :
                    smessage = 'connection lost ' + response.ErrorMessage if response.ErrorMessage else ''
                    time.sleep( scounter * 5 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError( response.ErrorMessage )
            else :
                # Connection lost. Give it 5, 10, 30 seconds and reconnect
                if sloop :
                    smessage = 'connection lost'
                    time.sleep( scounter * 5 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError('General connection error')                    

        return None


    def getsourcecode(self, scanid) :

        def execute():
            client, factory     = self.get_client_and_factory()
            return client.service.GetSourceCodeForScan(sessionID=self.__sessid, scanId=scanid)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None

        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST AUDIT recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST AUDIT recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST AUDIT error, "GetSourceCodeForScan"', e )
                if scounter > self.__retry :
                    raise e
                else :
                    sloop = True
            if response != None :
                if response.IsSuccesfull:
                    break
                # Token expired. Give it 2, 4, 8 seconds and get a new one
                elif not response.IsSuccesfull and ('12563' in response.ErrorMessage or 'Invalid_Token' in response.ErrorMessage) :
                    smessage = 'unauthorized  ' + response.ErrorMessage
                    time.sleep( scounter * 2 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Connection lost. Give it 5, 10, 15 seconds and reconnect
                elif sloop :
                    smessage = 'connection lost ' + response.ErrorMessage if response.ErrorMessage else ''
                    time.sleep( scounter * 5 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError( response.ErrorMessage )
            else :
                # Connection lost. Give it 5, 10, 30 seconds and reconnect
                if sloop :
                    smessage = 'connection lost'
                    time.sleep( scounter * 5 )
                    if self.__oauth :
                        self.get_auth_token()
                    else :
                        self.soap_logon()
                # Uuups. Something went wrong and can't recover
                else :
                    raise ValueError('General connection error')                    

        return response.sourceCodeContainer.ZippedFile

 