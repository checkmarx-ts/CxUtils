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


from scaapicaller import scaapi



class scaconn(object):

    def __init__(self):
        self.__host         = None
        self.__hostac       = None
        self.__tenant       = None
        self.__uname        = None
        self.__pword        = None
        self.__sca          = None
        self.__ac           = None
        self.__proxy        = None
        self.__proxyuser    = None
        self.__proxypass    = None

    def __init__(self, fqdn, aclfqdn, tenant, username, password, proxy_url = None, proxy_username = None, proxy_password = None ):
        self.__host         = fqdn.strip().lower().rstrip('/')
        self.__hostac       = aclfqdn.strip().lower().rstrip('/')
        self.__tenant       = tenant
        self.__uname        = username
        self.__pword        = password
        self.__sca          = None
        self.__ac           = None
        self.__proxy        = proxy_url
        self.__proxyuser    = proxy_username
        self.__proxypass    = proxy_password


    # --------------------------------------
    # Connectivity to the different SCA apis
    # --------------------------------------

    # SAST api connector
    @property
    def sca(self) :
        if not self.__sca :
            self.__sca = scaapi( self.__host, self.__hostac, self.__tenant, self.__uname, self.__pword, 'sca_api', 'sca_resource_owner', self.__proxy, self.__proxyuser, self.__proxypass )
        return self.__sca


    # Access control api connector
    @property
    def ac(self):
        if not self.__ac :
            self.__ac = scaapi( self.__hostac, self.__hostac, self.__tenant, self.__uname, self.__pword, 'access_control_api', 'sca_resource_owner', self.__proxy, self.__proxyuser, self.__proxypass )
        return self.__ac


    # Get sca access-control host
    @property
    def aclhostname(self) :
        return self.__hostac


    # Get sca host
    @property
    def hostname(self) :
        return self.sca.get_auth_token()
    

    def logon(self) :
        if self.__host == self.__hostac :
            self.ac.get_auth_token()
        else :
            self.sca.get_auth_token()


    # ---------------------
    # Permissions check
    # ---------------------
    def checkpermissions( self, perm_sca: bool = True, perm_accesscontrol: bool = False ) :
        auth_error = ''
        auth_sca = False
        auth_ac = False
        current_user = None
        all_permissions = []
        user_permissions = []

        # Get profile data for current user
        try :
            current_user = self.ac.get( '/myprofile' )
        except :
            raise Exception('Could not resolve logged user profile' )
        
        # Try get all permissions from ac
        try :
            all_permissions = self.ac.get( '/permissions' )
        except :
            all_permissions = []
        
        # Try get all roles from ac
        try :
            xroles = self.ac.get( '/roles' )
        except :
            xroles = []

        # Try get permissions for current user
        try:
            user = self.ac.get( '/users/' + str(current_user['id']) )
            for userrole in user['roleIds'] :
                xrole = next( filter( lambda el: el['id'] == int(userrole), xroles ), None )
                if xrole and xrole['name'] in ['Admin', 'SCA Admin', 'Access Control Manager'] :
                    auth_ac = True
                if xrole and xrole['name'] in ['Admin', 'SCA Admin', 'SCA Manager'] :
                    auth_sca = True
                user_permissions.extend(xrole['permissionIds'])
        except:
            pass
        user_permissions = set( user_permissions )

        if perm_sca and not auth_sca and len(user_permissions) > 0 and len(all_permissions) > 0 :
            xpermissions = list( filter( lambda el: el['id'] in user_permissions, all_permissions ) )
            if next( filter( lambda el: el['name'] == 'view', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'scan', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'create-project', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'edit-project', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'delete-project', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-risk', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'delete-scan', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-policy', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'administrate', xpermissions), None ) :
                auth_sca = True

        if perm_accesscontrol and not auth_ac and len(user_permissions) > 0 and len(all_permissions) > 0 :
            xpermissions = list( filter( lambda el: el['id'] in user_permissions, all_permissions ) )
            if next( filter( lambda el: el['name'] == 'manage-users', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-authentication-providers', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-clients', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-system-settings', xpermissions), None ) and \
              next( filter( lambda el: el['name'] == 'manage-roles', xpermissions), None ) :
                auth_ac = True


        # Authorization for SCA (admin)
        if perm_sca and not auth_sca :
            if auth_error :
                auth_error = auth_error + ', '
            auth_error = auth_error + 'SCA'

        # Authorization for access control: teams, roles, users, ac-config
        if perm_accesscontrol and not auth_ac :
            if auth_error :
                auth_error = auth_error + ', '
            auth_error = auth_error + 'access-control'
        
        # Finalization
        if auth_error :
            raise Exception('Connected user is not authorized to use: ' + auth_error )
        
        return True
