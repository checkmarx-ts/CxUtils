Add-Type -AssemblyName System.Web

function GetAuthHeaders ($session_token) {
    @{
        Authorization = $session_token.auth_header;
    }
}


function GetRestHeadersForRequest($session_token, $accept_type) {
    GetAuthHeaders $session_token + @{
        Accept = $accept_type;
    }
}

function GetRestHeadersForJsonRequest($session_token, $version) {
    $accept_type = 'application/json'
    
    if ([String]::IsNullOrEmpty($version) -ne $true)
    {
        $accept_type += ";v=$version"
    }

    GetRestHeadersForRequest $session_token $accept_type
}


function GetXFormUrlEncodedPayloadFromHashtable($table) {

    $query_builder = New-Object System.Text.StringBuilder
    $sep = ""

    $table.Keys | % { 
        [void]$query_builder.Append($sep).AppendFormat("{0}={1}", $_, $table.Item($_))
        $sep = "&"
    }

    $query_builder.ToString()
}


function GetQueryStringFromHashtable($table) {

    $query_builder = New-Object System.Text.StringBuilder
    $sep = ""

    $table.Keys | % { 
        [void]$query_builder.Append($sep).AppendFormat("{0}={1}", $_, [System.Web.HttpUtility]::UrlEncode($table.Item($_)))
        $sep = "&"
    }

    $query_builder.ToString()
}
