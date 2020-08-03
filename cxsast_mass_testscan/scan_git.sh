#Test command to use before running script on large amount of repos
#sh ./scan_git.sh test.txt
#only for CxFlow currently


folderexclusions="test,lib,docs,swagger,angular,node_modules,bootstrap,modernizer,yui,dojo,xjs,react,plugins,3rd,build,nuget"


echo "Cloning"
file=$1
lines=`cat $file`
for line in $lines; do
        git clone $line ./clonefolder        
        project=$(basename -s .git $line)
        echo "Cloned" $project
        java -jar cxflow.jar --spring.config.location="./application-scan.yml" --scan --f="./clonefolder" --cx-project=$project --app=$project --forcescan  --exclude-folders=$folderexclusions
        rm -rf *.zip
        rm -rf ./clonefolder
done