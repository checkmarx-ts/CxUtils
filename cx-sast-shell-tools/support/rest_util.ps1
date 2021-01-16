
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

function GetRestHeadersForJsonRequest($session_token) {
    GetRestHeadersForRequest $session_token 'application/json'
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
