#CxSAST Report Template setttings
#
#

@{
    reportType = "PDF"
    
    queries = @{
        all = 1
        ids = 0
    }

    resultSeverity = @{
        all = 0
        high = 1
        medium = 1
        low = 1
        info = 0
    }

    resultState = @{
        all = 1
        ids = 0
    }

    displayCategories = @{
        all = 1
        ids = 0
    }

    resultsAssignedTo = @{
        all = 1
        ids = 0
        usernames = 0
    }

    resultsPerVuln = @{
        all = 1
        max = 9999
    }

    headerOptions = @{
        link2online = 1
        team = 1
        version = 1
        scanComments = 1
        scanType = 1
        sourceOrigin = 1
        scanDensity = 1
    }

    generalOptions = @{
        onlyExecutiveSummary = 0
        tableOfContents = 1
        exectuiveSummary = 1
        displayCategories = 1
        displayLanguageHash = 0
        scannedQueries = 0
        scannedFiles = 1
        vulnDescriptions = "None"
    }

    resultsDisplayOption = @{
        assignedTo = 0
        comments = 0
        link2online = 0
        resultsDescription = 0
        snippetsMode = "None"
    }
}
