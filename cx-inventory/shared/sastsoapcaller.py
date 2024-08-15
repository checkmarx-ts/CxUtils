""" 
========================================================================

SIMPLE CLASS FOR AUDIT SOAP CALLS
Supports v8.8 and up

joao.costa@checkmarx.com
PS-EMEA
10-11-2022

========================================================================
"""

import time
import http
import requests
from requests import Session
from zeep import Client, Settings, xsd, helpers
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

relative_web_interface_url = "/CxWebInterface/Portal/CxWebService.asmx?wsdl"

class soapapi(object):

    def __init__(self):
        self.__token        = None
        self.__callcounter  = 0
        self.__retry        = 3
        self.__host         = None
        self.__uname        = None
        self.__pword        = None
        self.__scope        = None
        self.__client       = None
        self.__oauth        = None
        self.__sessid       = "0"
        self.__version      = None
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
        self.__oauth        = None
        self.__sessid       = "0"
        self.__version      = None
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


    def soap_logon(self) :
        def execute():
            client, factory     = self.get_client_and_factory(False)
            credentials = factory.Credentials(User=self.__uname, Pass=self.__pword )
            return client.service.Login(credentials, 1033)
        response = execute()
        if not response.IsSuccesfull :
            raise ValueError( response.ErrorMessage )
        self.__sessid = response.SessionId    
        return self.__sessid


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

            if self.__oauth == None :
                version = self.get_version().upper().replace('V','').strip()
                if version.startswith('8.') :
                    self.__oauth = False
                else :
                    self.__oauth = True

            if self.__oauth :
                if not self.__token :
                    self.get_auth_token()
                shead = { "Authorization":self.__token }
            elif self.__sessid == "0" :
                self.soap_logon()

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


    def get_version( self ) :
        if not self.__version :
            def execute():
                client, factory     = self.get_client_and_factory(False)
                return client.service.GetVersionNumber()
            response = execute()
            if not response.IsSuccesfull :
                raise ValueError( response.ErrorMessage )
            self.__version = response.Version       
        return self.__version


    def get_query_collection(self) :

        def execute():
            client, factory = self.get_client_and_factory()
            return client.service.GetQueryCollection(sessionId=self.__sessid)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None

        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "GetQueryCollection"', e )
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

        return {
            "IsSuccesfull": response.IsSuccesfull,
            "ErrorMessage": response.ErrorMessage,
            "QueryGroups": [
                {
                    "Description": query_group.Description,
                    "Impacts": query_group.Impacts,
                    "IsEncrypted": query_group.IsEncrypted,
                    "IsReadOnly": query_group.IsReadOnly,
                    "Language": query_group.Language,
                    "LanguageName": query_group.LanguageName,
                    "LanguageStateDate": query_group.LanguageStateDate,
                    "LanguageStateHash": query_group.LanguageStateHash,
                    "Name": query_group.Name,
                    "OwningTeam": query_group.OwningTeam,
                    "PackageFullName": query_group.PackageFullName,
                    "PackageId": query_group.PackageId,
                    "PackageType": query_group.PackageType,
                    "PackageTypeName": query_group.PackageTypeName,
                    "ProjectId": query_group.ProjectId,
                    "Queries": [
                        {
                            "Categories": [
                                {
                                    "CategoryName": category.CategoryName,
                                    "CategoryType": {
                                        "Id": category.CategoryType.Id,
                                        "Name": category.CategoryType.Name,
                                        "Order": category.CategoryType.Order,
                                    },
                                    "Id": category.Id
                                } for category in query.Categories.CxQueryCategory
                            ] if query.Categories else query.Categories,
                            "Cwe": query.Cwe,
                            "CxDescriptionID": query.CxDescriptionID,
                            "EngineMetadata": query.EngineMetadata,
                            "IsEncrypted": query.IsEncrypted,
                            "IsExecutable": query.IsExecutable,
                            "Name": query.Name,
                            "PackageId": query.PackageId,
                            "QueryId": query.QueryId,
                            "QueryVersionCode": query.QueryVersionCode,
                            "Severity": query.Severity,
                            "Source": query.Source,
                            "Status": query.Status,
                            "Type": query.Type,
                        } for query in query_group.Queries.CxWSQuery
                    ] if query_group.Queries else query_group.Queries,
                    "Status": query_group.Status
                } for query_group in response.QueryGroups.CxWSQueryGroup 
            ] if response.QueryGroups else response.QueryGroups
        }



    def getallqueries(self, detailed: bool = False) :
        queries = []

        response = self.get_query_collection()

        if not response.get("IsSuccesfull"):
            raise ValueError( response.get("ErrorMessage") )

        query_collection = response.get("QueryGroups")

        for group in query_collection :
            if group["Queries"] :
                for query in group.get("Queries") :
                    # All queries    
                    if not detailed :
                        qitem = { "QueryId":query.get("QueryId"), "Name":query.get("Name"), "LanguageName":group.get("LanguageName"), "PackageName":group.get("Name"), "PackageType":group.get("PackageType"), "PackageTypeName":group.get("PackageTypeName"), "OwningTeam":group.get("OwningTeam"), "ProjectId":group.get("ProjectId") }
                    else :
                        qitem = query
                        qitem["Language"] = group.get("Language") 
                        qitem["LanguageName"] = group.get("LanguageName") 
                        qitem["LanguageStateDate"] = group.get("LanguageStateDate") 
                        qitem["ProjectId"] = group.get("ProjectId") 
                        qitem["OwningTeam"] = group.get("OwningTeam") 
                        # qitem["PackageName"] = group.get("Name") 
                        qitem["PackageType"] = group.get("PackageType") 
                        qitem["PackageTypeName"] = group.get("PackageTypeName") 
                        qitem["PackageFullName"] = group.get("PackageFullName") 
                        qitem["PackageStatus"] = group.get("Status") 
                        qitem["GroupName"] = group.get("Name") 
                        qitem["GroupDescription"] = group.get("Description") 
                        qitem["GroupStatus"] = group.get("Status") 
                        qitem["Impacts"] = group.get("Impacts") 
                        qitem["IsEncrypted"] = group.get("IsEncrypted") 
                        qitem["IsReadOnly"] = group.get("IsReadOnly") 
                        qitem["Description"] = group.get("Description") 
                    queries.append(qitem)
        return queries



    def getcustomqueries(self) :
        queries = []

        response = self.get_query_collection()

        if not response.get("IsSuccesfull"):
            raise ValueError( response.get("ErrorMessage") )

        query_collection = response.get("QueryGroups")

        for group in query_collection :
            if group["Queries"] :
                for query in group.get("Queries") :
                    ptype = group.get("PackageType")
                    if (ptype == "Corporate") or (ptype == "Team") or (ptype == "Project") :
                        qitem = query
                        qitem["Language"] = group.get("Language") 
                        qitem["LanguageName"] = group.get("LanguageName") 
                        qitem["LanguageStateDate"] = group.get("LanguageStateDate") 
                        qitem["ProjectId"] = group.get("ProjectId") 
                        qitem["OwningTeam"] = group.get("OwningTeam") 
                        qitem["PackageName"] = group.get("Name") 
                        qitem["PackageType"] = group.get("PackageType") 
                        qitem["PackageTypeName"] = group.get("PackageTypeName") 
                        qitem["PackageFullName"] = group.get("PackageFullName") 
                        qitem["PackageStatus"] = group.get("Status") 
                        qitem["GroupName"] = group.get("Name") 
                        qitem["GroupDescription"] = group.get("Description") 
                        qitem["GroupStatus"] = group.get("Status") 
                        qitem["Impacts"] = group.get("Impacts") 
                        qitem["IsEncrypted"] = group.get("IsEncrypted") 
                        qitem["IsReadOnly"] = group.get("IsReadOnly") 
                        qitem["Description"] = group.get("Description") 
                        queries.append(qitem)
        return queries



    def getquerieslists(self) :
        
        queries = []        # All queries names
        qcustom = []        # All custom queries detailed

        response = self.get_query_collection()

        if not response.get("IsSuccesfull"):
            raise ValueError( response.get("ErrorMessage") )

        query_collection = response.get("QueryGroups")

        for group in query_collection :
            if group["Queries"] :
                for query in group.get("Queries") :
                    # All queries    
                    qitem = { "QueryId":query.get("QueryId"), "Name":query.get("Name"), "LanguageName":group.get("LanguageName"), "PackageType":group.get("PackageType"), "PackageTypeName":group.get("PackageTypeName"), "OwningTeam":group.get("OwningTeam"), "ProjectId":group.get("ProjectId") }
                    queries.append(qitem)
                    # Custom queries
                    ptype = group.get("PackageType")
                    if (ptype == "Corporate") or (ptype == "Team") or (ptype == "Project") :
                        qcust = query
                        qcust["Language"] = group.get("Language") 
                        qcust["LanguageName"] = group.get("LanguageName") 
                        qcust["LanguageStateDate"] = group.get("LanguageStateDate") 
                        qcust["ProjectId"] = group.get("ProjectId") 
                        qcust["OwningTeam"] = group.get("OwningTeam") 
                        qcust["PackageName"] = group.get("Name") 
                        qcust["PackageType"] = group.get("PackageType") 
                        qcust["PackageTypeName"] = group.get("PackageTypeName") 
                        qcust["PackageFullName"] = group.get("PackageFullName") 
                        qcust["PackageStatus"] = group.get("Status") 
                        qcust["GroupName"] = group.get("Name") 
                        qcust["GroupDescription"] = group.get("Description") 
                        qcust["GroupStatus"] = group.get("Status") 
                        qcust["Impacts"] = group.get("Impacts") 
                        qcust["IsEncrypted"] = group.get("IsEncrypted") 
                        qcust["IsReadOnly"] = group.get("IsReadOnly") 
                        qcust["Description"] = group.get("Description") 
                        qcustom.append(qcust)

        return queries, qcustom
    

    def getquerycategories(self) :

        categories = []
        def execute():
            client, factory = self.get_client_and_factory()
            return client.service.GetQueriesCategories(sessionId=self.__sessid)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "GetQueriesCategories"', e )
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
        
        category_collection = response.QueriesCategories.CxQueryCategory

        for ctg in category_collection :
            category = {}
            category['Id']                      = ctg.Id
            category['CategoryName']            = ctg.CategoryName
            category['CategoryType']            = {}
            category['CategoryType']['Id']      = ctg.CategoryType.Id
            category['CategoryType']['Name']    = ctg.CategoryType.Name
            category['CategoryType']['Order']   = ctg.CategoryType.Order
            categories.append(category)

        return categories



    def presetcreate( self, name, query_ids) :

        def execute():
            client, factory     = self.get_client_and_factory()
            query_id_list       = factory.ArrayOfLong(query_ids)
            cx_preset_detail    = factory.CxPresetDetails(
                queryIds=query_id_list, id=0, name=name, owningteam=1, isPublic=True,
                isUserAllowToUpdate=True, isUserAllowToDelete=True, IsDuplicate=False
            )
            return client.service.CreateNewPreset(sessionId=self.__sessid, presrt=cx_preset_detail)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "CreateNewPreset"', e )
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

        preset = response.preset
        if preset :
            return preset["id"] 
        else :
            return None


    def presetupdate( self, presetid, name, query_ids) :

        def execute():
            client, factory     = self.get_client_and_factory()
            query_id_list       = factory.ArrayOfLong(query_ids)
            cx_preset_detail    = factory.CxPresetDetails(
                queryIds=query_id_list, 
                id=presetid, 
                name=name, 
                owningteam=1, 
                isPublic=True,
                isUserAllowToUpdate=True, 
                isUserAllowToDelete=True, 
                IsDuplicate=False
            )
            return client.service.UpdatePreset(sessionId=self.__sessid, presrt=cx_preset_detail)    

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "UpdatePreset"', e )
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


    def projectgetdata( self, projectid ) :

        def execute():
            client, factory     = self.get_client_and_factory()
            return client.service.GetProjectConfiguration(sessionID=self.__sessid, projectID=projectid)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "GetProjectConfiguration"', e )
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

        output = {}

        # Resolve project settings
        settings = response.ProjectConfig.ProjectSettings
        projectid = settings['projectID']
        output['id']                    = projectid
        output['name']                  = settings['ProjectName']
        output['PresetID']              = settings['PresetID']
        # output['TaskId']: settings['TaskId']
        output['AssociatedGroupID']     = int(settings['AssociatedGroupID'])
        output['ScanConfigurationID']   = settings['ScanConfigurationID']
        output['Description']           = settings['Description']
        # output['Owner']                 = settings['Owner']
        output['IsPublic']              = settings['IsPublic']
        output['OpenSourceOrigin']      = settings['OpenSourceAnalysisOrigin']

        # Resolve source settings
        aux = None
        settings = response.ProjectConfig.SourceCodeSettings
        if settings :
            aux = {}
            aux['SourceOrigin']             = settings['SourceOrigin']
            aux['UserCredentials']          = { 'User': settings['UserCredentials']['User'], 'Pass': settings['UserCredentials']['Pass'] } if settings['UserCredentials'] else None
            aux['PathList']                 = [{ 'Path': item['Path'], 'IncludeSubTree': item['IncludeSubTree'] } for item in settings.PathList.ScanPath]
            aux['SourceControlCommandId']   = settings['SourceControlCommandId']
            aux['ExcludeFilesPatterns']     = settings.SourceFilterLists['ExcludeFilesPatterns']
            aux['ExcludeFoldersPatterns']   = settings.SourceFilterLists['ExcludeFoldersPatterns']
            aux['SourcePullingAction']      = settings['SourcePullingAction']
        output['SourceCodeSettings'] = aux

        # Resolve source control settings
        aux = None
        settings = response.ProjectConfig.SourceCodeSettings.SourceControlSetting
        if settings :
            aux = {}
            githubsettings = settings['GitHubSettings']
            if settings :
                aux['Port']                 = settings['Port']
                aux['UseSSL']               = settings['UseSSL']
                aux['UseSSH']               = settings['UseSSH']
                aux['ServerName']           = settings['ServerName']
                aux['Repository']           = settings['Repository']
                aux['UserCredentials']      = { 'User': settings['UserCredentials']['User'], 'Pass': settings['UserCredentials']['Pass'] } if settings['UserCredentials'] else None 
                aux['Protocol']             = settings['Protocol']
                aux['GITBranch']            = settings['GITBranch']
                aux['GITAuthentication']    = settings['GITAuthentication']
                aux['TFSAuthentication']    = settings['TFSAuthentication'] if settings['TFSAuthentication'] else 'None'
                aux['GitLsViewType']        = settings['GitLsViewType']
                aux['SSHPublicKey']         = settings['SSHPublicKey']
                aux['SSHPrivateKey']        = settings['SSHPrivateKey']
                aux['PerforceBrowsingMode'] = settings['PerforceBrowsingMode']
                aux['ProjectId']            = projectid
                aux['RepositoryName']       = settings['RepositoryName']
                aux['ProtocolParameters']   = settings['ProtocolParameters']
                if githubsettings :
                    gaux = {}
                    # ContributorSettings
                    csaux = None
                    if githubsettings['ContributorSettings'] :
                        csaux = {}
                        csaux['Repository']             = githubsettings['ContributorSettings']['Repository']
                        csaux['AuthenticationMethod']   = githubsettings['ContributorSettings']['AuthenticationMethod']
                        csaux['UserName']               = githubsettings['ContributorSettings']['UserName']
                        csaux['Token']                  = githubsettings['ContributorSettings']['Token']
                        csaux['PingUrl']                = githubsettings['ContributorSettings']['PingUrl']
                    gaux['ContributorSettings'] = csaux
                    # OwnerSettings
                    osaux = None
                    if githubsettings['OwnerSettings'] :
                        osaux = {} 
                        osaux['Repository']             = githubsettings['OwnerSettings']['Repository']
                        osaux['AuthenticationMethod']   = githubsettings['OwnerSettings']['AuthenticationMethod']
                        osaux['UserName']               = githubsettings['OwnerSettings']['UserName']
                        osaux['Token']                  = githubsettings['OwnerSettings']['Token']
                        osaux['PingUrl']                = githubsettings['OwnerSettings']['PingUrl']
                    gaux['OwnerSettings'] = osaux
                    # Other
                    gaux['EventsThreshold']         = githubsettings['EventsThreshold']
                    gaux['PingUrl']                 = githubsettings['PingUrl']
                    gaux['WebhookId']               = githubsettings['WebhookId']
                    aux['GitHubSettings'] = gaux
                else :
                    aux['GitHubSettings'] = None
        output['SourceControlSetting'] = aux

        # Resolve schedule settings
        aux = None
        settings = response.ProjectConfig.ScheduleSettings
        if settings :
            aux = {}
            aux['Schedule']                 = settings['Schedule']
            aux['SchedulingFrequency']      = settings['SchedulingFrequency']
            aux['ScheduledDays']            = settings['ScheduledDays'] if settings['ScheduledDays'] else None
            aux['Time']                     = settings['Time'] if settings['Time'] else None
            aux['StartSchedulingPeriod']    = settings['StartSchedulingPeriod'] if settings['StartSchedulingPeriod'] else None
            aux['EndSchedulingPeriod']      = settings['EndSchedulingPeriod'] if settings['EndSchedulingPeriod'] else None
        output['ScheduleSettings'] = aux

        # Resolve scan action settings
        aux = None
        settings = response.ProjectConfig.ScanActionSettings
        if settings :
            if settings.ScanActionList :
                aux = []
                for item in settings.ScanActionList.ScanAction :
                    action = { 'Action': item['Action'], 'Trigger': item['Trigger'], 'Parameters': item.Parameters.string }
                    # params = item.Parameters.string;
                    # for param in item.Parameters :
                    # #for param in item['Parameters'] :
                    #     params.append( {param['string']} )
                    # action['Parameters'] = params
                    aux.append(action)
        output['ScanActionSettings'] = aux

        # Resolve issue tracker settings
        aux = None
        settings = response.ProjectConfig.ProjectIssueTrackingSettings
        if settings :
            aux = {}
            aux['TrackingSystemID']         = settings['TrackingSystemID']
            params = None
            if settings.Params :
                params = []
                for item in settings.Params.CxWSIssueTrackingParam :
                    params.append( { 'Name': item['Name'], 'Value': item['Value'], 'Type': item['Type'] } )
            aux['Params']         = params
        output['ProjectIssueTrackingSettings'] = aux

        # Resolve custom fields
        aux = None
        settings = response.ProjectConfig.CustomFields
        if settings :
            aux = []
            for item in settings.CxWSProjectCustomField :
                aux.append( { 'CustomFieldId': item['CustomFieldId'], 'Value': item['Value'] } )
        output['CustomFields'] = aux

        # Resolve data retention settings
        aux = None
        settings = response.ProjectConfig.DataRetentionSettings
        if settings :
            aux = settings.NumOfScansToKeep
        output['DataRetentionSettings'] = aux

        return output



    def __internalprocessprojectdata(self, factory, projdata ) :

        project_settings = factory.ProjectSettings(
            projectID=projdata['id'],
            ProjectName=projdata['name'],
            PresetID=projdata['PresetID'],
            TaskId=0,
            AssociatedGroupID=projdata['AssociatedGroupID'],
            ScanConfigurationID=projdata['ScanConfigurationID'],
            Description=projdata['Description'] if projdata['Description'] else xsd.SkipValue,
            Owner=xsd.SkipValue,
            IsPublic=projdata['IsPublic'],
            OpenSourceSettings=xsd.SkipValue,
            OpenSourceAnalysisOrigin=projdata['OpenSourceOrigin']
        )

        github_settings = xsd.SkipValue
        if projdata['SourceControlSetting'] and projdata['SourceControlSetting']['GitHubSettings'] :
            settings = projdata['SourceControlSetting']['GitHubSettings']
            github_settings = factory.GitHubIntegrationSettings(
                ContributorSettings=factory.GithubSettings(
                    Repository=settings['ContributorSettings']['Repository'] if settings['ContributorSettings']['Repository'] else xsd.SkipValue,
                    AuthenticationMethod=settings['ContributorSettings']['AuthenticationMethod'],
                    UserName=settings['ContributorSettings']['UserName'] if settings['ContributorSettings']['UserName'] else xsd.SkipValue,
                    Token=settings['ContributorSettings']['Token'] if settings['ContributorSettings']['Token'] else xsd.SkipValue,
                    PingUrl=settings['ContributorSettings']['PingUrl'] if settings['ContributorSettings']['PingUrl'] else xsd.SkipValue
                    ) if settings['ContributorSettings'] else xsd.SkipValue,
                OwnerSettings=factory.GithubSettings(
                    Repository=settings['OwnerSettings']['Repository'] if settings['OwnerSettings']['Repository'] else xsd.SkipValue,
                    AuthenticationMethod=settings['OwnerSettings']['AuthenticationMethod'],
                    UserName=settings['OwnerSettings']['UserName'] if settings['OwnerSettings']['UserName'] else xsd.SkipValue,
                    Token=settings['OwnerSettings']['Token'] if settings['OwnerSettings']['Token'] else xsd.SkipValue,
                    PingUrl=settings['OwnerSettings']['PingUrl'] if settings['OwnerSettings']['PingUrl'] else xsd.SkipValue
                    ) if settings['OwnerSettings'] else xsd.SkipValue,
                EventsThreshold=settings['EventsThreshold'],
                PingUrl=settings['PingUrl'] if settings['PingUrl'] else xsd.SkipValue,
                WebhookId=settings['WebhookId']
            )

        source_control_setting=xsd.SkipValue
        if projdata['SourceControlSetting'] :
            settings = projdata['SourceControlSetting']
            source_control_setting = factory.SourceControlSettings(
                Port=settings['Port'],
                UseSSL=settings['UseSSL'],
                UseSSH=settings['UseSSH'],
                ServerName=settings['ServerName'] if settings['ServerName'] else xsd.SkipValue,
                Repository=settings['Repository'],
                UserCredentials=factory.Credentials(User=settings['UserCredentials']['User'], Pass=settings['UserCredentials']['Pass']) if settings['UserCredentials'] else xsd.SkipValue,
                Protocol=settings['Protocol'],
                RepositoryName=settings['RepositoryName'] if settings['RepositoryName'] else xsd.SkipValue,
                ProtocolParameters=settings['ProtocolParameters'] if settings['ProtocolParameters'] else xsd.SkipValue,
                GITBranch=settings['GITBranch'] if settings['GITBranch'] else xsd.SkipValue,
                GITAuthentication=settings['GITAuthentication'],
                TFSAuthentication=settings['TFSAuthentication'],
                GitLsViewType=settings['GitLsViewType'],
                SSHPublicKey=settings['SSHPublicKey'] if settings['SSHPublicKey'] else xsd.SkipValue,
                SSHPrivateKey=settings['SSHPrivateKey'] if settings['SSHPrivateKey'] else xsd.SkipValue,
                GitHubSettings=github_settings,
                PerforceBrowsingMode=settings['PerforceBrowsingMode'],
                ProjectId=projdata['id']
            )
        
        sourcecode_settings = xsd.SkipValue
        if projdata['SourceCodeSettings'] :
            settings = projdata['SourceCodeSettings']
            sourcecode_settings = factory.SourceCodeSettings(
                SourceOrigin=settings['SourceOrigin'],
                UserCredentials=factory.Credentials(User=settings['UserCredentials']['User'], Pass=settings['UserCredentials']['Pass']) if settings['UserCredentials'] else xsd.SkipValue,
                PathList=factory.ArrayOfScanPath([
                    factory.ScanPath(
                        Path=item['Path'], 
                        IncludeSubTree=item['IncludeSubTree'] 
                        ) for item in settings["PathList"]
                    ]) if settings["PathList"] else xsd.SkipValue,
                SourceControlSetting=source_control_setting,
                PackagedCode=xsd.SkipValue,
                SourcePullingAction=settings['SourcePullingAction'] if settings['SourcePullingAction'] else xsd.SkipValue,
                SourceControlCommandId=settings['SourceControlCommandId'],
                SourceFilterLists=factory.SourceFilterPatterns(
                    ExcludeFilesPatterns=settings['ExcludeFilesPatterns'] if settings['ExcludeFilesPatterns'] else xsd.SkipValue,
                    ExcludeFoldersPatterns=settings['ExcludeFoldersPatterns'] if settings['ExcludeFoldersPatterns'] else xsd.SkipValue,
                ) if settings['ExcludeFilesPatterns'] or settings['ExcludeFoldersPatterns'] else xsd.SkipValue
            )

        schedule_settings = xsd.SkipValue
        if projdata['ScheduleSettings'] :
            settings = projdata['ScheduleSettings']
            if settings['Schedule'] :
                schedule_settings = factory.ScheduleSettings(
                    Schedule=settings['Schedule'],
                    ScheduledDays=settings['ScheduledDays'] if settings['ScheduledDays'] else xsd.SkipValue,
                    Time=settings['Time'] if settings['Time'] else xsd.SkipValue,
                    StartSchedulingPeriod=settings['StartSchedulingPeriod'] if settings['StartSchedulingPeriod'] else xsd.SkipValue,
                    EndSchedulingPeriod=settings['EndSchedulingPeriod'] if settings['EndSchedulingPeriod'] else xsd.SkipValue,
                    SchedulingFrequency=settings['SchedulingFrequency']
                )
        
        scanaction_settings = xsd.SkipValue
        if projdata['ScanActionSettings'] :
            settings = projdata['ScanActionSettings']
            scanaction_settings = factory.ScanActionSettings(
                ScanActionList=factory.ArrayOfScanAction([ 
                    factory.ScanAction(
                        # Parameters=item['Parameters'], 
                        # Parameters=factory.ArrayOfString([pitem]) for pitem in item['Parameters'],
                        # Parameters=factory.ArrayOfString(item['Parameters']) if type(item['Parameters']) is list else item['Parameters'],
                        Parameters=factory.ArrayOfString(item['Parameters'] if type(item['Parameters']) is list else [item['Parameters']]),
                        Trigger=item['Trigger'], 
                        Action=item['Action']
                        )  for item in settings
                ])
            )

        def __issue_param_value( xtype, xvalue ) :
            if xvalue :
                if xtype == 'array' :
                    data = factory.ArrayOfAnyType()
                    for value in xvalue :
                        data['anyType'].append( xsd.AnyObject(helpers.guess_xsd_type(value), value)  )
                    return data

                    # return xsd.ComplexType(
                    #     xsd.Sequence(
                    #         [ xsd.AnyObject(helpers.guess_xsd_type(item), item) for item in xvalue ]
                    #     )
                    # )
                else :
                    return xsd.AnyObject(helpers.guess_xsd_type(xvalue), xvalue)
            else :
                return xsd.SkipValue

        issuetracker_settings = xsd.SkipValue
        if projdata['ProjectIssueTrackingSettings'] and projdata['ProjectIssueTrackingSettings']['TrackingSystemID'] > 0 : 
            settings = projdata['ProjectIssueTrackingSettings']
            issuetracker_settings = factory.CxWSProjectIssueTrackingSettings(
                TrackingSystemID=settings['TrackingSystemID'],
                Params=factory.ArrayOfCxWSIssueTrackingParam([
                    factory.CxWSIssueTrackingParam(
                        Name=item['Name'] if item['Name'] else xsd.SkipValue,
                        Value=__issue_param_value(item['Type'], item['Value'] ),
                        Type=item['Type'] if item['Type'] else xsd.SkipValue
                    ) for item in settings["Params"]
                ])
            )

        customfields_settings = xsd.SkipValue
        if projdata['CustomFields'] :
            settings = projdata['CustomFields']
            customfields_settings = factory.ArrayOfCxWSProjectCustomField([ 
                factory.CxWSProjectCustomField(
                    CustomFieldId=item['CustomFieldId'],
                    Value=item['Value'] if item['Value'] else xsd.SkipValue
                ) for item in settings
            ])

        dataretention_settings = xsd.SkipValue
        if projdata['DataRetentionSettings'] and projdata['DataRetentionSettings'] > 0 :
            dataretention_settings = factory.DataRetentionSettings(
                NumOfScansToKeep=projdata['DataRetentionSettings']  
            )    

        project_data = factory.ProjectConfiguration(
            ProjectSettings=project_settings,
            SourceCodeSettings=sourcecode_settings,
            ScheduleSettings=schedule_settings,
            ScanActionSettings=scanaction_settings,
            ProjectIssueTrackingSettings=issuetracker_settings,
            CustomFields=customfields_settings,
            DataRetentionSettings=dataretention_settings
        )

        return project_data        


    def projectcreate( self, projdata ) :

        def execute():
            client, factory     = self.get_client_and_factory()
            project_data = self.__internalprocessprojectdata( factory, projdata )
            return client.service.CreateNewProject(SessionID=self.__sessid, Project=project_data)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "CreateNewProject"', e )
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

        return



    def projectupdate( self, projdata ) :

        def execute():
            client, factory     = self.get_client_and_factory()
            project_data = self.__internalprocessprojectdata( factory, projdata )
            return client.service.UpdateProjectConfiguration(sessionID=self.__sessid, projectID=projdata['id'], projectConfiguration=project_data)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "UpdateProjectConfiguration"', e )
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

        return  



    def getresultsfromscan( self, scanid ) :

        def execute():
            client, factory = self.get_client_and_factory()
            return client.service.GetResultsForScan(sessionID=self.__sessid, scanId=scanid)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "GetResultsForScan"', e )
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

        if not response.Results :
            return []
        scan_results_list = response.Results.CxWSSingleResultData

        return [
                {
                    "QueryId": item["QueryId"],
                    "PathId": item["PathId"],
                    "SourceFolder": item["SourceFolder"],
                    "SourceFile": item["SourceFile"],
                    "SourceLine": item["SourceLine"],
                    "SourceObject": item["SourceObject"],
                    "DestFolder": item["DestFolder"],
                    "DestFile": item["DestFile"],
                    "DestLine": item["DestLine"],
                    "NumberOfNodes": item["NumberOfNodes"],
                    "DestObject": item["DestObject"],
                    "Comment": item["Comment"],
                    "State": item["State"],
                    "Severity": item["Severity"],
                    "AssignedUser": item["AssignedUser"],
                    "ConfidenceLevel": item["ConfidenceLevel"],
                    "ResultStatus": item["ResultStatus"],
                    "IssueTicketID": item["IssueTicketID"],
                    "QueryVersionCode": item["QueryVersionCode"]
                } for item in scan_results_list
            ] if scan_results_list else None



    def getcommentsfromresult( self, scanid, pathid ) :

        def execute():
            client, factory     = self.get_client_and_factory()
            return client.service.GetPathCommentsHistory(sessionId=self.__sessid, scanId=scanid, pathId=pathid, labelType='Remark')

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "GetPathCommentsHistory"', e )
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

        return response.Path.Comment



    def uploadtriages( self, triages ) :

        def execute():
            client, factory     = self.get_client_and_factory()
            triagedata=factory.ArrayOfResultStateData([
                factory.ResultStateData(
                    scanId=item['scanId'],
                    PathId=item['PathId'],
                    projectId=item['projectId'],
                    Remarks=item['Remarks'] if item['Remarks'] else xsd.SkipValue,
                    ResultLabelType=item['ResultLabelType'],
                    data=item['data']
                ) for item in triages 
            ])
            return client.service.UpdateSetOfResultState(sessionID=self.__sessid, resultsStates=triagedata)

        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "UpdateSetOfResultState"', e )
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

        return 
    
    def getresultstates( self ) :

        def execute(): 
            client, factory     = self.get_client_and_factory()
            return client.service.GetResultStateList(sessionID=self.__sessid)
        
        scounter: int   = 0
        response        = None
        sloop: bool     = False
        smessage: str   = None
        
        while (scounter <= self.__retry) :
            scounter += 1
            if scounter > 1 :
                if smessage :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) + ' after ' + smessage )
                else :
                    cxlogger.logwarning( 'SAST SOAP recover attempt ' + str(scounter-1) + '/' + str(self.__retry) )
                smessage = None

            try :
                response = execute()
            except Exception as e:
                # The connection may be closed by server, in such case, we want to try reconnect 
                cxlogger.logdebug( 'SAST SOAP error, "GetResultStateList"', e )
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

        result_states = response.ResultStateList.ResultState

        for result in result_states :
            if result['ResultID'] < 5 :
                result['IsCustom'] = False
            else :
                result['IsCustom'] = True
        
        return result_states