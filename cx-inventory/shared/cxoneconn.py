""" 
========================================================================

SIMPLE CLASS CXONE A INDEPENDENT CXONE
INCLUDES SUB-OBJECTS:
    .ast    for CXONE REST API calls
    .ac     for KEUCLOAK ACCESS-CONTROL REST API calls

joao.costa@checkmarx.com
PS-EMEA
22-12-2022

========================================================================
"""

import jwt
from cxoneapicaller import cxoneapi



class cxoneconn(object):

    def __init__(self):
        self.__tenant       = None
        self.__host         = None
        self.__keycloak     = None
        self.__apikey       = None
        self.__clientid     = None
        self.__granttype    = None
        self.__proxy        = None
        self.__proxyuser    = None
        self.__proxypass    = None
        self.__ast          = None
        self.__ac           = None
        self.__version      = None


    def __init__(self, fqdn, tenant, apikey, aclfqdn = None, clientid = None, granttype = None, proxy_url = None, proxy_username = None, proxy_password = None ) :
        self.__tenant       = tenant
        self.__host         = fqdn.strip().lower().rstrip('/')
        self.__keycloak     = None
        if aclfqdn :
            self.__keycloak = aclfqdn.strip().lower().rstrip('/')
        self.__apikey       = apikey
        self.__clientid     = clientid
        self.__granttype    = granttype
        self.__proxy        = proxy_url
        self.__proxyuser    = proxy_username
        self.__proxypass    = proxy_password
        self.__ast          = None
        self.__ac           = None
        self.__version      = None


    # ---------------------------------------
    # Connectivity to CXONE apis
    # ---------------------------------------

    # AST api connectors (all go the same way)
    @property
    def ast(self) :
        if not self.__ast :
            self.__ast = cxoneapi( self.__host, self.__tenant, self.__apikey, self.__keycloak, self.__clientid, self.__granttype, self.__proxy, self.__proxyuser, self.__proxypass, False )
        return self.__ast

    @property
    def cxone(self) :
        if not self.__ast :
            self.__ast = cxoneapi( self.__host, self.__tenant, self.__apikey, self.__keycloak, self.__clientid, self.__granttype, self.__proxy, self.__proxyuser, self.__proxypass, False )
        return self.__ast

    @property
    def ac(self) :
        if not self.__ac :
            self.__ac = cxoneapi( self.__host, self.__tenant, self.__apikey, self.__keycloak, self.__clientid, self.__granttype, self.__proxy, self.__proxyuser, self.__proxypass, True )
        return self.__ac

    @property
    def keycloak(self) :
        if not self.__ac :
            self.__ac = cxoneapi( self.__host, self.__tenant, self.__apikey, self.__keycloak, self.__clientid, self.__granttype, self.__proxy, self.__proxyuser, self.__proxypass, True )
        return self.__ac

    def logon(self) :
        if self.__host == self.__keycloak :
            self.ac.get_auth_token()
        else :
            self.cxone.get_auth_token()


    # ---------------------
    # Common configurations
    # ---------------------


    # Get cxone host
    @property
    def hostname(self) :
        return self.__host


    # Get cxone tenant
    @property
    def tenantname(self) :
        return self.__tenant
    

    # Get cxone version
    @property
    def version(self) :
        if (not self.__version) :
            try :
                try :
                    self.__version = self.cxone.get( '/api/versions') 
                except :
                    self.cxone.get_auth_token()
                    self.__version = self.cxone.get( '/api/versions') 
            except :
                self.__version = None
                pass
        # It wasn't found
        if (not self.__version) :
            self.__version = {}
            self.__version['KICS']  = ''
            self.__version['SAST']  = ''
        return self.__version

    

    @property
    def versionstring(self) :
        sversion = ''
        v = self.version
        if v['SAST'] :
            sversion = 'SAST: ' + v['SAST']
        if v['KICS'] :
            if sversion :
                sversion = sversion + ' & KICS: ' + v['KICS']
            else :
                sversion = 'KICS: ' + v['KICS']
        return sversion



    # ---------------------
    # Permissions check
    # ---------------------
    def checkpermissions( self, perm_cxone: bool = True, perm_accesscontrol: bool = False, perm_dast: bool = False ) :

        auth_error  = ''
        auth_cxone  = False
        auth_ac     = False
        auth_dast   = False

        if self.__host == self.__keycloak :
            token = self.ac.token()
        else :
            token = self.cxone.token()

        if not token :
            raise Exception('User is not authenticated' ) 

        # Decode the token and get the user id
        tokendata = jwt.decode( token, options={"verify_signature": False} )

        if tokendata :
            # userid = tokendata['sub']           # Subject
            if 'iam-admin' in tokendata['roles'] :
                auth_ac = True
            if 'ast-admin' in tokendata['roles_ast'] :
                auth_cxone = True
            if 'dast-admin' in tokendata['roles_ast'] :
                auth_dast = True

            if not auth_cxone and perm_cxone :
                if 'create-project' in tokendata['roles_ast'] and \
                  'view-projects' in tokendata['roles_ast'] and \
                  'delete-application' in tokendata['roles_ast'] and \
                  'delete-webhook' in tokendata['roles_ast'] and \
                  'delete-scan-if-in-group' in tokendata['roles_ast'] and \
                  'create-webhook' in tokendata['roles_ast'] and \
                  'ast-scanner' in tokendata['roles_ast'] and \
                  'update-scan' in tokendata['roles_ast'] and \
                  'my_test_role' in tokendata['roles_ast'] and \
                  'delete-query' in tokendata['roles_ast'] and \
                  'update-feedbackapp' in tokendata['roles_ast'] and \
                  'delete-project' in tokendata['roles_ast'] and \
                  'view-project-params' in tokendata['roles_ast'] and \
                  'delete-pool' in tokendata['roles_ast'] and \
                  'create-pool' in tokendata['roles_ast'] and \
                  'open-feature-request' in tokendata['roles_ast'] and \
                  'view-policy-management' in tokendata['roles_ast'] and \
                  'ast-risk-manager' in tokendata['roles_ast'] and \
                  'update-tenant-params' in tokendata['roles_ast'] and \
                  'view-queries' in tokendata['roles_ast'] and \
                  'manage-webhook' in tokendata['roles_ast'] and \
                  'create-feedbackapp' in tokendata['roles_ast'] and \
                  'update-pool' in tokendata['roles_ast'] and \
                  'access-iam' in tokendata['roles_ast'] and \
                  'create-application' in tokendata['roles_ast'] and \
                  'queries-editor' in tokendata['roles_ast'] and \
                  'view-results' in tokendata['roles_ast'] and \
                  'update-query' in tokendata['roles_ast'] and \
                  'delete-feedbackapp' in tokendata['roles_ast'] and \
                  'update-result-not-exploitable' in tokendata['roles_ast'] and \
                  'update-project' in tokendata['roles_ast'] and \
                  'view-engines' in tokendata['roles_ast'] and \
                  'delete-scan' in tokendata['roles_ast'] and \
                  'create-query' in tokendata['roles_ast'] and \
                  'update-result' in tokendata['roles_ast'] and \
                  'view-preset' in tokendata['roles_ast'] and \
                  'update-policy-management' in tokendata['roles_ast'] and \
                  'update-preset' in tokendata['roles_ast'] and \
                  'delete-policy-management' in tokendata['roles_ast'] and \
                  'view-webhooks' in tokendata['roles_ast'] and \
                  'update-access' in tokendata['roles_ast'] and \
                  'manage-policy-management' in tokendata['roles_ast'] and \
                  'open-support-ticket' in tokendata['roles_ast'] and \
                  'ast-viewer' in tokendata['roles_ast'] and \
                  'view-access' in tokendata['roles_ast'] and \
                  'manage-feedbackapp' in tokendata['roles_ast'] and \
                  'view-pools' in tokendata['roles_ast'] and \
                  'delete-preset' in tokendata['roles_ast'] and \
                  'view-applications' in tokendata['roles_ast'] and \
                  'update-application' in tokendata['roles_ast'] and \
                  'view-license' in tokendata['roles_ast'] and \
                  'update-project-params' in tokendata['roles_ast'] and \
                  'create-preset' in tokendata['roles_ast'] and \
                  'view-feedbackapp' in tokendata['roles_ast'] and \
                  'create-policy-management' in tokendata['roles_ast'] and \
                  'order-services' in tokendata['roles_ast'] and \
                  'manage-project' in tokendata['roles_ast'] and \
                  'view-tenant-params' in tokendata['roles_ast'] and \
                  'view-scans' in tokendata['roles_ast'] and \
                  'create-scan' in tokendata['roles_ast'] and \
                  'manage-access' in tokendata['roles_ast'] and \
                  'manage-application' in tokendata['roles_ast'] and \
                  'update-webhoo' in tokendata['roles_ast'] :
                    auth_cxone = True

            if not auth_dast and perm_dast :
                if 'dast-delete-scan' in tokendata['roles_ast'] and \
                  'dast-cancel-scan' in tokendata['roles_ast'] and \
                  'dast-update-scan' in tokendata['roles_ast'] and \
                  'dast-create-environment' in tokendata['roles_ast'] and \
                  'dast-update-results' in tokendata['roles_ast'] and \
                  'dast-create-scan' in tokendata['roles_ast'] and \
                  'dast-external-scans' in tokendata['roles_ast'] :
                    auth_dast = True

            if not auth_ac and perm_accesscontrol :
                if 'manage-users' in tokendata['roles'] and \
                  'offline_access' in tokendata['roles'] and \
                  'manage-keys' in tokendata['roles'] and \
                  'uma_authorization' in tokendata['roles'] and \
                  'manage-groups' in tokendata['roles'] and \
                  'user' in tokendata['roles'] and \
                  'manage-clients' in tokendata['roles'] :
                    auth_ac = True

        # Authorization for CXONE (admin)
        if perm_cxone and not auth_cxone :
            if auth_error :
                auth_error = auth_error + ', '
            auth_error = auth_error + 'CXONE'

        # Authorization for IAM
        if perm_accesscontrol and not auth_ac :
            if auth_error :
                auth_error = auth_error + ', '
            auth_error = auth_error + 'IAM'

        # Authorization for DAST
        if perm_dast and not auth_dast :
            if auth_error :
                auth_error = auth_error + ', '
            auth_error = auth_error + 'DAST'
        
        # Finalization
        if auth_error :
            raise Exception('Connected user is not authorized to use: ' + auth_error )                
        
        return True

