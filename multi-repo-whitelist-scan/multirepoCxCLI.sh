mkdir clonefolder && cd clonefolder
echo "Cloning"
file="../giturls.txt"
lines=`cat $file`
for line in $lines; do
        git clone $line
done
cd ..
echo "Cloning Complete"

echo "Whitelisting"
mkdir ScanDir
find ./clonefolder -type f -regex ".*\.\(sln\|csproj\|cs\|xaml\|cshtml\|javasln\|project\|java\|jsp\|jspf\|xhtml\|jsf\|tld\|tag\|mf\|js\|html\|htm\|apex\|apexp\|page\|component\|cls\|trigger\|tgr\|object\|report\|workflow\|\-meta\.xml\|cpp\|c\+\+\|cxx\|hpp\|hh\|h\+\+\|hxx\|c\|cc\|h\|vb\|vbs\|asp\|bas\|frm\|cls\|dsr\|ctl\|vb\|vbp\|php\|php3\|php4\|php5\|phtm\|phtml\|tpl\|ctp\|twig\|rb\|rhtml\|rxml\|rjs\|erb\|lock\|pl\|pm\|plx\|psgi\|m\|h\|xib\|pls\|sql\|pkh\|pks\|pkb\|pck\|py\|gtl\|groovy\|gsh\|gvy\|gy\|gsp\|properties\|aspx\|asax\|ascx\|master\|config\|xml\|cgi\|inc\)" -exec cp --parents \{\} ./ScanDir \;
rm -rf clonefolder
echo "Whitelisting Complete"

echo "Scanning"
sh ./CxConsolePlugin-8.90.2/runCxConsole.sh Scan -v -Projectname "$PROJECT" -CxServer $CXSERVER -CxToken $CXTOKEN -LocationType folder -LocationPath ../ScanDir  -locationpathexclude '*test*,*lib*,*node_modules*,*swagger*'
rm -rf ScanDir
