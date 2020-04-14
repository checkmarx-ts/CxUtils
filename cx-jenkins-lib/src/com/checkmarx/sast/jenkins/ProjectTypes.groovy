package com.checkmarx.sast.jenkins

/**
 * 
 * Workaround for lack of enum support in Jenkins Pipelines
 * 
 * @author randy@checkmarx.com
 *
 */
class ProjectTypes {
    
    static final String WebApp = ProjectType.WebApp.toString()
    static final String WebService = ProjectType.WebService.toString()
    static final String Mobile = ProjectType.Mobile.toString()
    
    static int lookupPreset(String projectType) {
        int result
        switch (projectType) {
            case WebApp :
                result = ProjectType.WebApp.getPresetId()
                break;
            case WebService :
                result = ProjectType.WebService.getPresetId()
                break;
            case Mobile :
                result = ProjectType.Mobile.getPresetId()
                break;
            default : 
                result = ProjectType.WebApp.getPresetId()
                break
        }
        return result
    }

}
