# Define o caminho do diretório que você deseja analisar
param (
    [string]$basedir
)

#"D:\Users\nuno.rocha\Desktop\CLI\SFLY\3529-dci-portal-aliaswire-service-20221021163844-1021107"
$base_directory_path = $basedir

#####################################
$ignoreList = @(
".ActiveScans",
".SourceControl",
"CxSourceHash._cx_",
"MethodsMapping.zip"
)
$exclusionFolderList = @(
    "test", # Tests
    "mock", # Tests
    "spec", # Tests
    "unit", # Tests
    "debug", # Tests
    "e2e", #Tests
    "androidTest", # Tests (Android)
    "build", # Build Folders
    "dist", # Build Folders
    "deploy", # Build Folders
    "venv", # Build Folders (Python)
    "maven", # Build Folders
    "gradle", # Build Folders (Android)
    "target", # Build Folders
    "example", # Dead Code
    "sample", # Dead Code
    "bin", # Non-relevant folders
    "gen", # Non-relevant folders
    "docs", # Non-relevant folders
    "proguard", # Non-relevant folders (Android)
    "lint", # Non-relevant folders
    "images", # Non-relevant folders
    "swagger", # Non-relevant folders (Swagger)
    "coverage", # Non-relevant folders
    "generated", # Non-relevant folders
    ".vs", # Non-relevant folders (Visual Studio)
    ".idea", # Non-relevant folders (IntelliJ IDEA)
    ".temp", # Non-relevant folders (Temporary)
    ".tmp", # Non-relevant folders (Temporary)
    ".grunt", # Non-relevant folders (Grunt)
    ".cache", # Non-relevant folders (Cache)
    ".dynamodb", # Non-relevant folders (Dinamo DB)
    ".fusebox", # Non-relevant folders (Fusebox)
    ".serverless", # Non-relevant folders (Serverless)
    ".nyc_output", # Non-relevant folders (NYC)
    ".git", # Non-relevant folders (Git)
    ".github", # Non-relevant folders (Github)
    ".dependabot", # Non-relevant folders (Dependabot)
    ".semaphore", # Non-relevant folders (Semaphore CI)
    ".circleci", # Non-relevant folders (Circle CI)
    ".vscode", # Non-relevant folders (VS Code)
    ".nuget", # Non-relevant folders (CSharp)
    ".mvn", # Non-relevant folders (Maven)
    ".m2", # Non-relevant folders (Maven)
    ".DS_Store", # Non-relevant folders
    ".sass-cache", # Non-relevant folders
    ".gradle", # Non-relevant folders (Android)
    "__pycache__", # Non-relevant folders (Python)
    ".pytest_cache", # Non-relevant folders (Python)
    ".settings", # Non-relevant folders (CSharp)
    "imageset", # Non-relevant folders (IOS)
    "xcuserdata", # Non-relevant folders (IOS)
    "xcshareddata", # Non-relevant folders (IOS)
    "xcassets", # Non-relevant folders (IOS)
    "appiconset", # Non-relevant folders (IOS)
    "xcodeproj", # Non-relevant folders (IOS)
    "framework", # Non-relevant folders (IOS)
    "lproj", # Non-relevant folders (IOS)
    "__MACOSX", # Non-relevant folders (IOS)
    "css", # CSS not supported
    "react", #3rd Party Libraries (React)
    "yui", #3rd Party Libraries
    "node_modules", #3rd Party Libraries (Node JS)
    "jquery", #3rd Party Libraries (JS)
    "angular", #3rd Party Libraries (JS)
    "bootstrap", #3rd Party Libraries (JS)
    "modernizr", #3rd Party Libraries (JS)
    "bower_components", #3rd Party Libraries (Bower)
    "jspm_packages", #3rd Party Libraries (JS)
    "typings",  #3rd Party Libraries (Typescript)
    "dojo", #3rd Party Libraries
    "package", #3rd Party Libraries (CSharp)
    "vendor", #3rd Party Libraries (Golang)
    "xjs" #3rd Party Libraries (JS)
)
$exclusionFileList = @(
    "min.js", # 3rd Party Libraries (JS)
    "spec", # Tests (JS/Typescript/Node JS)
    "test", # Tests
    "mock" # Tests
)
$3rdpartyExclusionFileList = @(
    "license",
    "copyright" 
)


#####################################
#
# analisar filename for excludable pattern
#
#####################################
function isFileExcludable($file_path){
	# Extrai o nome do arquivo do caminho do arquivo
	$file_name = Split-Path $file_path -Leaf

	# Extrai o nome do arquivo sem a extensão
	$base_name = [System.IO.Path]::GetFileNameWithoutExtension($file_name)

	# Extrai a extensão do arquivo
	$extension = [System.IO.Path]::GetExtension($file_name)

	# Exibe os resultados
	#Write-Host "Nome do arquivo: $file_name"
	#Write-Host "Nome base do arquivo: $base_name"
	#Write-Host "Extensão do arquivo: $extension"
	
	# does filename match the exclusion pattern?
	foreach($exclusionFile in $exclusionFileList){
                if($file_name -match $exclusionFile){
                    return $true;
                }
	}
	# does file have any content that indicates it is possible to be excluded?
	
	return isFileContainsKeyword($file_path);
}

####################################
#
# verifica se um file contem um palavra chave nas primeiras 10 linhas
# $arquivo_path - Define o caminho do arquivo 
#
#####################################
function isFileContainsKeyword($arquivo_path ){
	#Write-Host "--- analisando ficheiro $arquivo_path "
	$options = [System.StringComparison]::InvariantCultureIgnoreCase
	
	foreach ($palavra_procurada in $3rdpartyExclusionFileList) {
		# Lê as primeiras 10 linhas do arquivo e procura pela palavra
		$resultado = Get-Content -Path $arquivo_path -TotalCount 10 | Select-String -Pattern $palavra_procurada #-SimpleMatch -Options $options

		# Verifica se a palavra foi encontrada nas primeiras 10 linhas
		if ($resultado) {
			#Write-Host "A palavra '$palavra_procurada' foi encontrada nas primeiras 10 linhas do arquivo."		
			return $true;
		} 
	}
	#Write-Host "Nenhuma palavra-chave não foi encontrada nas primeiras 10 linhas do arquivo."
	return $false;	
}

#####################################
#
# analisar foldername for excludable pattern
#
#####################################
function isFolderExcludable($file_path){
	#Write-Host " --- analisando folder $file_path "
	foreach($exclusionFolder in $exclusionFolderList){
            if($file_path -match $exclusionFolder){                
                return $true;
            }
        }
	return $false;
}

#####################################
#
# verificar se file esta contido numa pasta excluida
#
#####################################
function isFileUnderExcludedFolder{
	param(
			[string]$file_path,
			[string[]]$folder_exclusion_list
		)

	foreach($directory_path in $folder_exclusion_list){
		#Write-Host "Verificar se $file_path esta dentro de $directory_path"
		#if (Test-Path $file_path -PathType Leaf -ea SilentlyContinue) {
		if (  ($file_path.StartsWith($directory_path)) -and ($file_path -ne $directory_path ) ) {
			return $true;
		} 
	}	
	return $false;
}

#####################################
#
# Remover prefixo em todas a strings duma lista
#
#####################################
function removePrefix{
	param(
			[string[]]$myList,
			[string]$prefixToRemove
	)
	
	$new_list = New-Object System.Collections.Generic.List[string]
	foreach($str in $myList){		
		#Write-Host "------------------------------ $str"
		if ($str.StartsWith($prefixToRemove)) {
			$str = $str.Remove(0, $prefixToRemove.Length)
		}
		#Write-Host "------------------------------ $str"
		$new_list.Add($str)
	}
	
	return $new_list
}

#####################################
#
# main
#
#####################################
$file_exclusion_list = New-Object System.Collections.Generic.List[string]
$folder_exclusion_list = New-Object System.Collections.Generic.List[string]
# Obtém todos os arquivos e pastas dentro do diretório
$items = Get-ChildItem $base_directory_path -Recurse

# Itera sobre cada item dentro do diretório
foreach ($item in $items) {
    # Extrai o nome do item
    $name = $item.Name
    $fullname = $item.FullName
	$skipFlag = $false;
	
	foreach($ignore in $ignoreList){
		if($name -eq $ignore){
			$skipFlag=$true
		}
	}
	if($skipFlag) {
		continue
	}
	
    # Extrai o tipo do item (arquivo ou pasta)
    if ($item.PSIsContainer) {
        #$type = "Pasta"
		if (isFolderExcludable($name)){
			#Write-Host " adicionar $fullname à lista de exclusões de folder"
			$folder_exclusion_list.Add($fullname)
		}
    }
    else {
        #$type = "Arquivo"
		if(isFileUnderExcludedFolder($fullname, $folder_exclusion_list)){
			#Write-Host " SKIP"		
			continue #skip
		}
		
		if( isFileExcludable($fullname)){
			#Write-Host " adicionar $fullname à lista de exclusões de ficheiros"			
			$file_exclusion_list.Add($fullname)			
		}
    }
}

# Clean up folders  within excluded folders 
$folders_in_excluded_folder_list = New-Object System.Collections.Generic.List[string]
foreach($folder_path in $folder_exclusion_list){
	#Write-Host "Re-Validar ficheiro $folder_path  "
		# Check if the file is under the directory
		
		$flag = isFileUnderExcludedFolder $folder_path   $folder_exclusion_list 
		
		if ($flag) {
			#Write-Host "Sim, folder $folder_path  esta dentro duma pasta excluida"
			# remove file from exclusion list
			$folders_in_excluded_folder_list.Add($folder_path )			
		} 
}
foreach($folder_path in $folders_in_excluded_folder_list){
	$var = $folder_exclusion_list.Remove($folder_path)	
}
# Clean up files within excluded folders 
$files_in_excluded_folder_list = New-Object System.Collections.Generic.List[string]
foreach($file_path in $file_exclusion_list){
	#Write-Host "Re-Validar ficheiro $file_path "
		# Check if the file is under the directory
		
		$flag = isFileUnderExcludedFolder $file_path  $folder_exclusion_list 
		
		if ($flag) {
			#Write-Host "Sim, ficheiro $file_path esta dentro duma pasta excluida"
			# remove file from exclusion list
			$files_in_excluded_folder_list.Add($file_path)
			
		} 
}
foreach($file_path in $files_in_excluded_folder_list){
	$var = $file_exclusion_list.Remove($file_path)	
}

#remover o basepase de todas as strings
$file_exclusion_list = removePrefix $file_exclusion_list $basedir
$folder_exclusion_list = removePrefix $folder_exclusion_list $basedir

# output results
Write-Host "------------------------------"
Write-Host "File Exclusions:"
$file_exclusion_list_concatenada = $file_exclusion_list -join"; "
Write-Host $file_exclusion_list_concatenada 
Write-Host "------------------------------"

Write-Host "Folder Exclusions:"
$folder_exclusion_list_concatenada = $folder_exclusion_list -join"; "
Write-Host $folder_exclusion_list_concatenada
Write-Host "------------------------------"

<# END #>