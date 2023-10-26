package com.freddiemac.cxone.vmar;

import java.time.LocalDateTime;
import java.util.Date;

import com.fasterxml.jackson.annotation.*;

@JsonIgnoreProperties(ignoreUnknown = true)
public class scansMetaData {
    public scansMetaData(){};
    private String scanId;
    public String getscanId(){
            return scanId;
    }
    public void setscanId(String scanId){
            this.scanId=scanId;
    }
    private String projectId;
    public String getprojectId(){
            return projectId;
    }
    public void setprojectId(String projectId){
            this.projectId=projectId;
    }
     private String projectName;
     public String getprojectName() {
             return projectName;
     }
     public void setprojectName(String projectName) {
             this.projectName = projectName;
     }
     private String assetId; 
     public String getassetId() {
             return assetId;
     }
     public void setassetId(String assetId) {
             this.assetId = assetId;
     }
     private String methodology;  
     public String getmethodology() {
             return methodology;
     }
     public void setmethodology(String methodology) {
             this.methodology = methodology;
     }   
     private String tags;
     public String gettags(){
                return tags;
     }
     public void settags(String tags){
                this.tags=tags;
     }
    private String sor; 
    public String getsor() {
            return sor;
    }
    public void setsor(String sor) {
            this.sor = sor;
    }
    private String scanSource;    
    public String getscanSource() {
            return scanSource;
    }
    public void setscanSource(String scanSource) {
            this.scanSource = scanSource;
    }
    private String codeRepo; 
    public String getcodeRepo() {
            return codeRepo;
    }
    public void setcodeRepo(String codeRepo) {
            this.codeRepo = codeRepo;
    }
    private String buildNumber;   
    public String getbuildNumber() {
            return buildNumber;
    }
    public void setbuildNumber(String buildNumber) {
            this.buildNumber = buildNumber;
    }
    private String pipelineName;  
    public String getpipelineName() {
            return pipelineName;
    }
    public void setpipelineName(String pipelineName) {
            this.pipelineName = pipelineName;
    }
    private String commitId; 
    public String getcommitId() {
            return commitId;
    }
    public void setcommitId(String commitId) {
            this.commitId = commitId;
    }
    private String latest;   
    public String getlatest() {
            return latest;
    }
    public void setlatest(String latest) {
            this.latest = latest;
    }
    ////
    private String prodDeployed;  
    public String getprodDeployed() {
            return prodDeployed;
    }
    public void setprodDeployed(String prodDeployed) {
            this.prodDeployed = prodDeployed;
    }
    ////
    private LocalDateTime prodDeployedDate;   
    public LocalDateTime getprodDeployedDate() {
            return prodDeployedDate;
    }
    public void setprodDeployedDate(LocalDateTime prodDeployedDate) {
            this.prodDeployedDate = prodDeployedDate;
    }
    //////
    private String releaseTicketNumber;
    public String getreleaseTicketNumber() {
            return releaseTicketNumber;
    }
    public void setreleaseTicketNumber(String releaseTicketNumber) {
            this.releaseTicketNumber = releaseTicketNumber;
    }
    ///
    private String releaseTicketStatus;
    public String getreleaseTicketStatus() {
            return releaseTicketStatus;
    }
    public void setreleaseTicketStatus(String releaseTicketStatus) {
            this.releaseTicketStatus = releaseTicketStatus;
    }
    ///
    private String similarityId;  
    public String getsimilarityId() {
            return similarityId;
    }
    public void setsimilarityId(String similarityId) {
            this.similarityId = similarityId;
    }
    private String queryName;
    public String getqueryName() {
            return queryName;
    }
    public void setqueryName(String queryName) {
            this.queryName = queryName;
    }
    private String queryDescription;   
    public String getqueryDescription() {
            return queryDescription;
    }
    public void setqueryDescription(String queryDescription) {
            this.queryDescription = queryDescription;
    }
    private String severity; 
    public String getseverity() {
            return severity;
    }
    public void setseverity(String severity) {
            this.severity = severity;
    }
    private String scanDate; 
    public String getscanDate() {
            return scanDate;
    }
    public void setscanDate(String scanDate) {
            this.scanDate = scanDate;
    }
    private String cweId;    
    public String getcweId() {
            return cweId;
    }
    public void setcweId(String cweId) {
            this.cweId = cweId;
    }
    // SCA specific
    private String packageName;   
    public String getpackageName() {
            return packageName;
    }
    public void setpackageName(String packageName) {
            this.packageName = packageName;
    }
    private String packageVersion;
    public String getpackageVersion() {
            return packageVersion;
    }
    public void setpackageVersion(String packageVersion) {
            this.packageVersion = packageVersion;
    }
    private String cveId;    
    public String getcveId() {
            return cveId;
    }
    public void setcveId(String cveId) {
            this.cveId = cveId;
    }
    private String cveDescription;
    public String getcveDescription(){
        return cveDescription;
    }
    public void setcveDescription(String cveDescription){
        this.cveDescription=cveDescription;
    }
    private String majorVersion;  
    public String getmajorVersion() {
            return majorVersion;
    }
    public void setmajorVersion(String majorVersion) {
            this.majorVersion = majorVersion;
    }
    private String minorVersion;  
    public String getminorVersion() {
            return minorVersion;
    }
    public void setminorVersion(String minorVersion) {
            this.minorVersion = minorVersion;
    }
  /*    private String severity;
    public String getseverity(){
        return severity;
    }
    public void setseverity(String severity){
        this.severity=severity;
    }
.addColumn("majorVersion")
.addColumn("minorVersion")
.addColumn("severity")
*/
}
