package com.checkmarx.sast.jenkins

class LineOfBusiness {

    enum LoB {
        AppSec('AppSec'),
        IT ('IT'),
		// add additional BUs 
    
        LoB(String fullname) {
            this.fullname = fullname
        }
    
        private final String fullname
        String getFullname() {
            fullname
        }
    }
    
    static final String AppSec = LoB.AppSec
    static final String IT = LoB.IT
	// add additional BUs
    
    static def LoB parse(String lob) {
        return lob as LoB
    }
}
