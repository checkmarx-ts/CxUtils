""" 
========================================================================

SIMPLE CLASS SAST A INDEPENDENT CXSAST
INCLUDES SUB-OBJECTS:
    .sast   for SAST REST API calls
    .ac     for ACCESS-CONTROL SAST REST API calls
    .odata  for ODATA API calls
    .soap   for SAST SOAP calls
    .audit  for AUDIT SOAP calls

joao.costa@checkmarx.com
PS-EMEA
10-11-2022

========================================================================
"""


from sastapicaller import sastapi
from sastsoapcaller import soapapi
from sastauditcaller import auditapi



class sastconn(object):

    def __init__(self):
        self.__host         = None
        self.__uname        = None
        self.__pword        = None
        self.__sast         = None
        self.__ac           = None
        self.__odata        = None
        self.__soap         = None
        self.__audit        = None
        self.__proxy        = None
        self.__proxyuser    = None
        self.__proxypass    = None
        self.__version      = None

    def __init__(self, fqdn, username, password, proxy_url = None, proxy_username = None, proxy_password = None ):
        self.__host         = fqdn.strip().lower().rstrip('/')
        self.__uname        = username
        self.__pword        = password
        self.__sast         = None
        self.__ac           = None
        self.__odata        = None
        self.__soap         = None
        self.__audit        = None
        self.__proxy        = proxy_url
        self.__proxyuser    = proxy_username
        self.__proxypass    = proxy_password
        self.__version      = None


    # ---------------------------------------
    # Connectivity to the different SAST apis
    # ---------------------------------------

    # SAST api connector
    @property
    def sast(self) :
        if not self.__sast :
            self.__sast = sastapi( self.__host, self.__uname, self.__pword, 'sast_rest_api', 'resource_owner_client', self.__proxy, self.__proxyuser, self.__proxypass )
        return self.__sast

    # Access control api connector
    @property
    def ac(self):
        if not self.__ac :
            self.__ac = sastapi( self.__host, self.__uname, self.__pword, 'access_control_api', 'resource_owner_client', self.__proxy, self.__proxyuser, self.__proxypass )
        return self.__ac

    # Odata api connector
    @property
    def odata(self):
        if not self.__odata :
            self.__odata = sastapi( self.__host, self.__uname, self.__pword, 'access_control_api sast_api', 'resource_owner_sast_client', self.__proxy, self.__proxyuser, self.__proxypass )
        return self.__odata

    # Soap api connector
    @property
    def soap(self):
        if not self.__soap :
            self.__soap = soapapi( self.__host, self.__uname, self.__pword, 'offline_access sast_api', 'resource_owner_sast_client', self.__proxy, self.__proxyuser, self.__proxypass )
        return self.__soap

    # Audit soap api connector
    @property
    def audit(self):
        if not self.__audit :
            self.__audit = auditapi( self.__host, self.__uname, self.__pword, 'offline_access sast_api', 'resource_owner_sast_client', self.__proxy, self.__proxyuser, self.__proxypass )
        return self.__audit

    def logon(self) :
        self.sast.get_auth_token()


    # ---------------------
    # Common configurations
    # ---------------------

    # Get sast version
    @property
    def version(self) :
        # Attempt to get the version using REST API (v9.0 and up)
        if (not self.__version) :
            try :
                self.__version = self.sast.get('/cxrestapi/system/version')
                data = self.sast.get('/cxrestapi/sast/engineservers')
                if (len(data) >= 1):
                    self.__version['enginePack'] = data[0].get('cxVersion')
                else:  
                    self.__version['enginePack'] = ''
            except :
                self.__version = None
                pass
        # Attempt to get the version using SOAP (v8.9 and down)
        if (not self.__version) :
            try :
                hotfix = '0'
                ver = self.soap.get_version().upper().replace('V','').strip()
                hfp = ver.index('HF')
                if hfp :
                    hotfix = ver[hfp + 2:]
                    ver    = ver[:hfp]
                if ver :
                    self.__version = {}
                    self.__version['version']       = ver.strip()
                    self.__version['hotFix']        = hotfix.strip()
                    self.__version['enginePack']    = ''
            except :
                self.__version = None
                pass
        # It wasn't found
        if (not self.__version) :
            self.__version = {}
            self.__version['version']       = '0'
            self.__version['hotFix']        = ''
            self.__version['enginePack']    = ''
        return self.__version


    # Get sast version as string
    @property
    def versionstring(self, withoutbuild = True) :
        version = ''
        v = self.version
        if (v) and (v['version']):
            fullv = v['version']
            if withoutbuild :
                splited = fullv.split('.')
                if len(splited) > 3 :
                    version += splited[0] + '.' + splited[1] + '.' + splited[2]
                else :
                    version += fullv
            else :
                version += fullv
        if (v) and (v['hotFix']):
            version += ' HF' + v['hotFix']
        if (v) and (v['enginePack']):
            version += ' EP' + v['enginePack']
        return version


    # Get sast host
    @property
    def hostname(self) :
        return self.__host



    # ---------------------
    # Permissions check
    # ---------------------
    def checkpermissions( self, perm_sast: bool = True, perm_accesscontrol: bool = False, perm_odata: bool = False, perm_audit: bool = False, read_only: bool = False ) :
        auth_error = ''
        auth_sast = False
        auth_ac = False
        auth_odata = False
        auth_audit = False
        current_user = None
        all_permissions = []
        user_permissions = []

        # Get profile data for current user
        try :
            current_user = self.ac.get( '/cxrestapi/auth/myprofile' )
        except :
            raise Exception('Could not resolve logged user profile' )
        
        # Try get all permissions from ac
        try :
            all_permissions = self.ac.get( '/cxrestapi/auth/permissions' )
        except :
            all_permissions = []
        # Try get all roles from ac
        try :
            xroles = self.ac.get( '/cxrestapi/auth/roles' )
        except :
            xroles = []

        # Try get permissions for current user
        try:
            user = self.ac.get( '/cxrestapi/auth/users/' + str(current_user['id']) )
            for userrole in user['roleIds'] :
                xrole = next( filter( lambda el: el['id'] == int(userrole), xroles ), None )
                if xrole and xrole['name'] in ['Admin', 'Access Control Manager'] :
                    auth_ac = True
                if xrole and xrole['name'] in ['Admin', 'SAST Admin'] :
                    auth_sast = True
                user_permissions.extend(xrole['permissionIds'])
        except:
            pass
        user_permissions = set( user_permissions )

        if perm_sast and not auth_sast and len(user_permissions) > 0 and len(all_permissions) > 0 :
            xpermissions = list( filter( lambda el: el['id'] in user_permissions, all_permissions ) )
            if read_only :
                if next( filter( lambda el: el['name'] == 'view-failed-sast-scan', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'download-scan-log', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'download-system-logs', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-data-analysis-templates', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'generate-scan-report', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'export-scan-results', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'view-results', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'see-support-link', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-data-retention', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-engine-servers', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-system-settings', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-external-services-settings', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-custom-fields', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-issue-tracking-systems', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-pre-post-scan-actions', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-custom-description', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-result-assignee', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'update-project', xpermissions), None ) :
                    auth_sast = True
            else :
                if next( filter( lambda el: el['name'] == 'save-sast-scan', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'delete-sast-scan', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'save-project', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'delete-project', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'view-failed-sast-scan', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'download-scan-log', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'download-system-logs', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-data-analysis-templates', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'generate-scan-report', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-result-comment', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-result-severity', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'open-issue-tracking-tickets', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'export-scan-results', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'view-results', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'see-support-link', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-data-retention', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-engine-servers', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-system-settings', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-external-services-settings', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-custom-fields', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-issue-tracking-systems', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-pre-post-scan-actions', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-custom-description', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'create-preset', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'update-and-delete-preset', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'update-project', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'create-project', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'manage-result-assignee', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'set-result-state-toverify', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'set-result-state-notexploitable', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'set-result-state-confirmed', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'set-result-state-urgent', xpermissions), None ) and \
                    next( filter( lambda el: el['name'] == 'set-result-state-proposednotexploitable', xpermissions), None ) :
                    auth_sast = True


        if perm_accesscontrol and not auth_ac and len(user_permissions) > 0 and len(all_permissions) > 0 :
            xpermissions = list( filter( lambda el: el['id'] in user_permissions, all_permissions ) )
            if next( filter( lambda el: el['name'] == 'manage-users', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-authentication-providers', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-clients', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-system-settings', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-roles', xpermissions), None ) :
                auth_ac = True

        # Authorization for SAST (admin)
        if perm_sast and not auth_sast :
            if auth_error :
                auth_error = auth_error + ', '
            auth_error = auth_error + 'SAST'

        # Authorization for access control: teams, roles, users, ac-config
        if perm_accesscontrol and not auth_ac :
            if auth_error :
                auth_error = auth_error + ', '
            auth_error = auth_error + 'access-control'
        
        # Authorization for ODATA
        if perm_odata :
            # Check if the permission is there first
            if len(user_permissions) > 0 and len(all_permissions) > 0 :
                for permission in user_permissions :
                    perm = next( filter( lambda el: el['id'] == permission, all_permissions), None )
                    if perm and  perm['name'] == 'use-odata' :
                        auth_odata  = True
            # Do an ODATA call to check if it responds
            else :
                try :
                    self.odata.get('/Cxwebinterface/odata/v1/Projects?$top=1&$skip=0' )
                    auth_odata  = True
                except :
                    pass
            if not auth_odata :
                if auth_error :
                    auth_error = auth_error + ', '
                auth_error = auth_error + 'ODATA'

        # Authorization for CxAudit 
        if perm_audit :
            # Check if the permission is there first
            if len(user_permissions) > 0 and len(all_permissions) > 0 :
                for permission in user_permissions :
                    perm = next( filter( lambda el: el['id'] == permission, all_permissions), None )
                    if perm and  perm['name'] == 'use-cxaudit' :
                        auth_audit = True
            # Do an AUDIT call to check if it responds
            else :
                try:
                    auth_audit = self.audit.getlicensedetails()
                except :
                    pass
            if not auth_audit :
                if auth_error :
                    auth_error = auth_error + ', '
                auth_error = auth_error + 'CxAudit'

        # Finalization
        if auth_error :
            raise Exception('Connected user is not authorized to use: ' + auth_error )
        
        return True
