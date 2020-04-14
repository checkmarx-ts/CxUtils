#!/bin/sh

function debug() { if [ "${DEBUG}" = "1" ]; then echo "[DEBUG] $*"; fi; }
function info() { echo "[INFO ] $*"; }
function warning { echo "[WARN ] $*"; }
function error() { echo "[ERROR] $*"; }

# Default CxFlow properties
CXFLOW_JAR="$(find / -name 'cx-flow*.jar')"
CXFLOW_CONFIG="/application.yml"
CXFLOW_MODE="scan"
CXFLOW_BREAK="false"
CXFLOW_PATH="$(pwd)"
CXFLOW_AUTODOWNLOADER=0
# Default Checkmarx properties
CHECKMARX_URI="$CHECKMARX_URI"
CHECKMARX_USER="$CHECKMARX_USER"
CHECKMARX_PASSWORD="$CHECKMARX_PASSWORD"
CHECKMARX_PROJECT="$CHECKMARX_PROJECT"
CHECKMARX_XML_PATH="./Checkmarx/Reports/ScanReport.xml"
# Default Azure properties
AZURE_URL="$SYSTEM_TEAMFOUNDATIONCOLLECTIONURI"
AZURE_PROJECT="$BUILD_REPOSITORY_NAME"
AZURE_BRANCH="$BUILD_SOURCEBRANCHNAME"
AZURE_TEAM="$SYSTEM_TEAMPROJECT"
AZURE_BUGTYPE="issue"


# Parse all the arguments
for arg in "$@"
do
    case $arg in
        # CxFlow parameters
        -j=*|--cxflow-jar=*)
            CXFLOW_JAR="${arg#*=}"; shift
        ;;
        -c=*|--cxflow-config=*)
            CXFLOW_CONFIG="${arg#*=}"; shift
        ;;
        -m=*|--cxflow-mode=*)
            CXFLOW_MODE="${arg#*=}"; shift
        ;;
        -b=*|--cxflow-break=*)
            CXFLOW_BREAK="${arg#*=}"; shift
        ;;
        -p=*|--cxflow-path=*)
            CXFLOW_PATH="${arg#*=}"; shift
        ;;
        # Checkmarx based variables
        --checkmarx-uri=*)
            CHECKMARX_URI="${arg#*=}"; shift
        ;;
        --checkmarx-user=*)
            CHECKMARX_USER="${arg#*=}"; shift
        ;;
        --checkmarx-password=*)
            CHECKMARX_PASSWORD="${arg#*=}"; shift
        ;;
        --checkmarx-project=*)
            CHECKMARX_PROJECT="${arg#*=}"; shift
        ;;
        --checkmarx-xml-path=*)
            CHECKMARX_XML_PATH="${arg#*=}"; shift
        ;;
        --cxflow-autodownload)
            CXFLOW_AUTODOWNLOADER=1; shift
        ;;
        # Azure
        --azure-url=*)
            AZURE_URL="${arg#*=}"; shift
        ;;
        --azure-project=*)
            AZURE_PROJECT="${arg#*=}"; shift
        ;;
        --azure-branch=*)
            AZURE_BRANCH="${arg#*=}"; shift
        ;;
        --azure-team=*)
            AZURE_TEAM="${arg#*=}"; shift
        ;;
        --azure-bugtype=*)
            AZURE_BUGTYPE="${arg#*=}"; shift
        ;;
        # Unknown
        *)
            error "Unknown argument: $1"; shift
            exit 1
        ;;
    esac
done


echo "   _____             ______ _"
echo "  / ____|           |  ____| |                      /\\"
echo " | |    __  ________| |__  | | _____      ________ /  \    _____   _ _ __ ___ "
echo " | |    \\ \\/ /______|  __| | |/ _ \ \ /\ / /______/ /\ \  |_  / | | | '__/ _ \\"
echo " | |____ >  <       | |    | | (_) \ V  V /      / ____ \  / /| |_| | | |  __/"
echo "  \_____/_/\_\      |_|    |_|\___/ \_/\_/      /_/    \_\/___|\__,_|_|  \___|"
echo "                                                                              "
echo ""

debug "Debug is enabled"

# TODO: Auto-downloader
if [[ ! -f "$CXFLOW_JAR" ]]; then
    if [[ "$CXFLOW_AUTODOWNLOADER" == 1 ]]; then
        error "Feature not supported: Auto-downloader"
        exit 1
    fi
    error "CxFlow Jar not found at: $CXFLOW_JAR"
    exit 1
else
    debug "CxFlow Jar found"
fi

if [[ -f "$CHECKMARX_XML_PATH" ]]; then
    # If the XML report file exists, the plugin or CLI have executed
    # before CxFlow. In this case, we want to run CxFlow in Parsing
    # mode and pick up the file to create tickets.
    debug "Running in 'parse' mode"

    CXFLOW_MODE="parse"
    CXFLOW_PATH="$CHECKMARX_XML_PATH"
fi

# Config as Code
CXFLOW_CONFIGASCODE="$CXFLOW_PATH/cx.config"
if [[ -f "$CXFLOW_CONFIGASCODE" ]]; then
    # Setting flag
    CONFIGASCODE="--config=\"$CXFLOW_CONFIGASCODE\""
else
    debug "No Config was found, set to null"
    CONFIGASCODE=""
fi

if [[ -z "$CHECKMARX_PROJECT" ]]; then
    # If the Project name isn't passed in, use the Git Repo project
    debug "Using name from pipeline as CHECKMARX_PROJECT is not set"
    CHECKMARX_PROJECT="$BUILD_REPOSITORY_NAME"
fi

if [[ "$CXFLOW_MODE" == "scan" ]]; then
    # Test if there are any files/folders being passed into the eviroment (including Docker).
    # If "0" is returned, not files are present.
    debug "Scan mode enabled"
    debug "Checking - files/folders in working directory"
    if [ "$(ls -i $CXFLOW_PATH | wc -l)" -eq "0" ]; then
        error "No files/folders in working directory..."
        exit 1
    fi
else
    debug "No files needed as running in parse/project mode"
fi

# Encryption Algorithm
if [[ ! -z "$CXFLOW_KEY" ]]; then
    info "Jasypt is being used to decrypt sensitive information"
    JASYPT_ENCRYPTOR_PASSWORD="$CXFLOW_KEY"
    # Default algorithm support
    if [[ -z "$CXFLOW_KEY_ALGORITHM" ]]; then
        JASYPT_ENCRYPTOR_ALGORITHM="PBEWITHHMACSHA512ANDAES_256"
    else
        JASYPT_ENCRYPTOR_ALGORITHM="$CXFLOW_KEY_ALGORITHM"
    fi
else
    debug "Not using Jasypt to decrypt tokens..."
fi


# CxFlow properties
debug "CxFlow Jar        :: $CXFLOW_JAR"
info  "CxFlow Mode       :: $CXFLOW_MODE"
info  "CxFlow Break      :: $CXFLOW_BREAK"
debug "CxFlow WorkingDir :: $CXFLOW_PATH"
debug "CxFlow ConfAsCode :: $CXFLOW_CONFIGASCODE"
debug "CxFlow KeyAlg     :: $JASYPT_ENCRYPTOR_ALGORITHM"
# Checkmarx properties
info  "Checkmarx URI     :: $CHECKMARX_URI"
debug "Checkmarx User    :: $CHECKMARX_USER"
info  "Checkmarx Project :: $CHECKMARX_PROJECT"
# Azure properties
debug "Azure URL         :: $AZURE_URL"
info  "Azure Project     :: $BUILD_REPOSITORY_NAME"
info  "Azure Branch      :: $BUILD_SOURCEBRANCHNAME"
info "Azure Team        :: $SYSTEM_TEAMPROJECT"


# This will execute CxFlow will settings from the Azure pipeline
java \
    -Xms512m -Xmx2048m \
    -Djava.security.egd=file:/dev/./urandom \
    -jar ${CXFLOW_JAR} \
    --spring.config.location="$CXFLOW_CONFIG" \
    ${CONFIGASCODE} \
    --${CXFLOW_MODE} \
    --app="$AZURE_PROJECT" \
    --namespace="$AZURE_TEAM" \
    --repo-name="$AZURE_PROJECT" \
    --branch="$AZURE_BRANCH" \
    --cx-project="$CHECKMARX_PROJECT" \
    --checkmarx.base-url="$CHECKMARX_URI" \
    --checkmarx.username="$CHECKMARX_USER" \
    --checkmarx.password="$CHECKMARX_PASSWORD" \
    --cx-flow.break-build="$CXFLOW_BREAK" \
    --azure.url="$AZURE_URL" \
    --azure.issue-type="$AZURE_BUGTYPE" \
    --bug-tracker="Azure" \
    --f="$CXFLOW_PATH"

info "CxFlow exiting..."
