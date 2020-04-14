package com.checkmarx.sast.jenkins

/**
 * Provides standardized methods for scanning source code in the Jenkins workspace 
 * with Checkmarx CxSAST and CxOSA scanners.
 * 
 * Based on original Cx library by Nitya Narasimhan (nnarasi3@checkmarx.com)
 * 
 * See: https://checkmarx.atlassian.net/wiki/spaces/KC/pages/129646534/Configuring+a+CxSAST+Scan+Action+using+Jenkins+Pipeline+v8.5.0+to+v8.8.0
 *  
 * @author randy@checkmarx.com
 *
 */
class CxScan implements Serializable {

    private static final String ORG = 'CxServer'
    private static final String SP = 'Checkmarx'
    private static final String PATH_SEP = '\\'

    // rjg: enums don't work in Pipelines
    //final LineOfBusiness lob
    //final ProjectType projectType
    //private LineOfBusiness.LoB group

    // required fields
    final def script
    final String lob
    final String projectType
    final String applicationID
    final String applicationName
    final String applicationTeam
    final String componentName
    final String branch
    final String environment
    
    // Optional properties with defaults
    String sourceEncoding = '1'                 // default engine configuration
    boolean avoidDuplicateProjectScans = true
    boolean failBuildOnNewResults = false
    String failBuildOnNewSeverity = 'HIGH'

    // optional vulnerability threshold fields, call enableVulnerabilityThreshold method to set
    private boolean vulnerabilityThresholdEnabled = false
    private String vulnerabilityThresholdResult = 'UNSTABLE'
    private int vulnerabilityHighThreshold = 0
    
    // Required fields that can be appended to
    private String comment = 'CommitID=${GIT_COMMIT}; URL=${GIT_URL}; Branch=${GIT_BRANCH}; Committer=${GIT_COMMITTER_NAME}'
    private String excludeFolders = 'node_modules,test,target'
    private String filterPattern = '''
            !**/_cvs/**/*, !**/.svn/**/*,   !**/.hg/**/*,   !**/.git/**/*,  !**/.bzr/**/*, !**/bin/**/*,
            !**/obj/**/*,  !**/backup/**/*, !**/.idea/**/*, !**/*.DS_Store, !**/*.ipr,     !**/*.iws,
            !**/*.bak,     !**/*.tmp,       !**/*.aac,      !**/*.aif,      !**/*.iff,     !**/*.m3u, !**/*.mid, !**/*.mp3,
            !**/*.mpa,     !**/*.ra,        !**/*.wav,      !**/*.wma,      !**/*.3g2,     !**/*.3gp, !**/*.asf, !**/*.asx,
            !**/*.avi,     !**/*.flv,       !**/*.mov,      !**/*.mp4,      !**/*.mpg,     !**/*.rm,  !**/*.swf, !**/*.vob,
            !**/*.wmv,     !**/*.bmp,       !**/*.gif,      !**/*.jpg,      !**/*.png,     !**/*.psd, !**/*.tif, !**/*.swf,
            !**/*.jar,     !**/*.zip,       !**/*.rar,      !**/*.exe,      !**/*.dll,     !**/*.pdb, !**/*.7z,  !**/*.gz,
            !**/*.tar.gz,  !**/*.tar,       !**/*.gz,       !**/*.ahtm,     !**/*.ahtml,   !**/*.fhtml, !**/*.hdm,
            !**/*.hdml,    !**/*.hsql,      !**/*.ht,       !**/*.hta,      !**/*.htc,     !**/*.htd, !**/*.war, !**/*.ear,
            !**/*.htmls,   !**/*.ihtml,     !**/*.mht,      !**/*.mhtm,     !**/*.mhtml,   !**/*.ssi, !**/*.stm,
            !**/*.stml,    !**/*.ttml,      !**/*.txn,      !**/*.xhtm,     !**/*.xhtml,   !**/*.class, !**/*.iml, !Checkmarx/Reports/*.*
            '''

    // Computed fields
    final String teamPath
    final String projectName
    
    // OSA properties
    String osaArchiveIncludePatterns = '*.zip, *.war, *.ear, *.tgz'
    
    

    public CxScan(script, String lob, String projectType, String applicationTeam, String applicationID,
            String applicationName, String componentName, String branch, String environment) {

        this.script = script
        this.lob = lob
        this.projectType = projectType
        this.applicationTeam = applicationTeam
        this.applicationID = applicationID
        this.applicationName = applicationName
        this.componentName = componentName
        this.branch = branch
        this.environment = environment
        this.teamPath = PATH_SEP + ORG + PATH_SEP + SP + PATH_SEP + lob + PATH_SEP + applicationTeam
        this.projectName = "${applicationName}-${componentName}-${branch}"
        this.comment = "ApplicationID: ${applicationID}; Jenkins build #: ${script.env.BUILD_NUMBER}"
    }

    private void addExclusions(String excludeFolders, String filterPattern) {
        this.excludeFolders += excludeFolders ? ',' + excludeFolders : ''
        this.filterPattern += filterPattern ? ',' + filterPattern : ''
    }

    void addFolderExclusions(String excludeFolders) {
        addExclusions(excludeFolders, '')
    }

    void addFilterPattern(String filterPattern) {
        addExclusions('', filterPattern)
    }
    
    void addScanComment(String comment) {
        this.comment += comment ? '; ' + comment : '' 
    }
    
    /**
     * Use to enable vulnerability threshold
     * 
     * @param failBuild - if true, build will FAIL; otherwise build will be UNSTABLE
     * @param highThreshold - set to number of high results to trigger threshold 
     */
    void enableVulnerabilityThreshold(boolean failBuild, int highThreshold) {
        this.vulnerabilityThresholdEnabled = true
        this.vulnerabilityThresholdResult = failBuild ? 'FAILURE' : 'UNSTABLE'
        this.vulnerabilityHighThreshold = highThreshold 
    }

    /**
     * Perform a full synchronous SAST scan; no PDF report 
     */
    def doFullScan() {
        doFullScan(true, false)
    }

    /**
     * Perform a full SAST scan; specify sync/async, no PDF report 
     */
    def doFullScan(boolean syncScan) {
        doFullScan(syncScan, false)
    }

    /**
     * Perform a full SAST scan; specify sync/async, PDF report 
     */
    def doFullScan(boolean syncScan, boolean generatePDF) {
        doScan(false, syncScan, generatePDF)
    }
    
    /**
     * Perform an incremental synchronous SAST scan; no PDF report 
     */
    def doIncrementScan() {
        doIncrementScan(true, false)
    }

    /**
     * Perform an incremental SAST scan; specify sync/async, no PDF report 
     */
    def doIncrementScan(boolean syncScan) {
        doIncrementScan(syncScan, false)
    }

    /**
     * Perform an incremental SAST scan; specify sync/async, PDF report 
     */
    def doIncrementScan(boolean syncScan, boolean generatePDF) {
        doScan(true, syncScan, generatePDF)
    }

    /**
     * Perform a SAST scan; specify incremental, sync/async, PDF report 
     */
    def doScan(boolean incremental, boolean syncScan, boolean generatePDF) {
        printConfig(incremental, syncScan, generatePDF)

        script.steps.step([$class: 'CxScanBuilder',
            useOwnServerCredentials: false, 
            avoidDuplicateProjectScans: this.avoidDuplicateProjectScans, 
            comment: this.comment,
            teamPath: this.teamPath, 
            incremental: incremental,
            exclusionsSetting: 'job', 
            excludeFolders: this.excludeFolders, 
            filterPattern: this.filterPattern,
            preset: ProjectTypes.lookupPreset().toString(), 
            projectName: this.projectName, 
            sourceEncoding: this.sourceEncoding,            // engine configuration
            generatePdfReport: generatePDF,
            failBuildOnNewResults: this.failBuildOnNewResults, 
            failBuildOnNewSeverity: this.failBuildOnNewSeverity,
            highThreshold: this.vulnerabilityHighThreshold,
            vulnerabilityThresholdEnabled: this.vulnerabilityThresholdEnabled,
            vulnerabilityThresholdResult: this.vulnerabilityThresholdResult,
            waitForResultsEnabled: syncScan,
            osaEnabled: false])
    }
    
    
    // TODO: implement correctly for v8.8
    def doOsaScan(String includeFolders, String excludeFolders) {
        printOsaConfig(includeFolders, excludeFolders)
        
        script.echo 'WARNING: OSA scan not implemented yet....'

        /*
        script.steps.step([$class: 'CxScanBuilder',
            useOwnServerCredentials: false, 
            avoidDuplicateProjectScans: this.avoidDuplicateProjectScans, 
            comment: this.comment,
            teamPath: this.teamPath, 
            incremental: false,
            exclusionsSetting: 'job', 
            excludeFolders: this.excludeFolders, 
            filterPattern: this.filterPattern,
            preset: ProjectTypes.lookupPreset().toString(), 
            projectName: this.projectName, 
            sourceEncoding: this.sourceEncoding,            // engine configuration
            generatePdfReport: generatePDF,
            failBuildOnNewResults: this.failBuildOnNewResults, 
            failBuildOnNewSeverity: this.failBuildOnNewSeverity,
            highThreshold: this.vulnerabilityHighThreshold,
            vulnerabilityThresholdEnabled: this.vulnerabilityThresholdEnabled,
            vulnerabilityThresholdResult: this.vulnerabilityThresholdResult,
            waitForResultsEnabled: true,
            excludeOpenSourceFolders: excludeFolders,
            includeOpenSourceFolders: includeFolders,
            osaArchiveIncludePatterns: this.osaArchiveIncludePatterns, 
            osaEnabled: true, 
            osaInstallBeforeScan: false])
           */
    }
    
    def printConfig(boolean incremental, boolean syncScan, boolean generatePDF) {

        def message = """\
            Running scan...
            \tLineOfBusiness: $lob
            \tProjectType: $projectType
            \tApplicationID: $applicationID
            \tApplicationName: $applicationName
            \tApplicationTeam: $applicationTeam
            \tComponentName: $componentName
            \tBranch: $branch
            \tEnvironment: $environment
            \tTeamPath: $teamPath
            \tProjectName: $projectName
            \tIncremental: $incremental
            \tSynchronous: $syncScan
            \tGeneratePDF: $generatePDF
            \tComment: ${ this.comment }
            \tFailBuildOnNewResults: ${ this.failBuildOnNewResults }
            \tFailBuildOnNewSeverity: ${ this.failBuildOnNewSeverity }
            \tVulnerabilityThresholdEnabled: ${ this.vulnerabilityThresholdEnabled }
            \tVulnerabilityThresholdResult: ${ this.vulnerabilityThresholdResult }
            \tVulnerabilityHighThreshold: ${ this.vulnerabilityHighThreshold }
            \tExcludeFolders: ${ this.excludeFolders }
            \tFilterPattern: ${ this.filterPattern }
            """
        script.echo message
    }
    
    def printOsaConfig(String includeFolders, String excludeFolders) {

        def message = """
            Running OSA scan...
            \tLineOfBusiness: $lob
            \tProjectType: $projectType
            \tApplicationID: $applicationID
            \tApplicationName: $applicationName
            \tApplicationTeam: $applicationTeam
            \tComponentName: $componentName
            \tBranch: $branch
            \tEnvironment: $environment
            \tTeamPath: $teamPath
            \tProjectName: $projectName
            \tIncludeFolders: $includeFolders
            \tExcludeFolders: $excludeFolders
            \tOsaArchiveIncludePatterns: $osaArchiveIncludePatterns
            """
        script.echo message
    }
    
}
