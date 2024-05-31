$cp=chcp "1251"
function Get-MWTitleByPID{
[CmdletBinding()]
param (
    [Parameter(
        Mandatory = $true,
        Position = 1,
        ValueFromPipeline = $true,
        ValueFromPipelineByPropertyName = $true,
        ValueFromRemainingArguments = $true,
        HelpMessage = "process id of process which title you want to obtain")]
    [Alias("PID")]
    [String[]]$ProcessID
)
BEGIN{

}

PROCESS{
    $t=Get-Process | Where-Object {$_.Id.ToString() -eq $ProcessID};
    write-output $t.MainWindowTitle
}
}
Get-MWTitleByPID $args[0]
