if ((Get-Command "fuck").CommandType -eq "Function") {
	fuck @args;
	[Console]::ResetColor()
	exit
}

"First time use of thefuck detected. "

if ((Get-Content $PROFILE -Raw -ErrorAction Ignore) -like "*thefuck*") {
} else {
	"  - Adding thefuck intialization to user `$PROFILE"
	$script = "`n`$env:PYTHONIOENCODING='utf-8' `niex `"`$(thefuck --alias)`"";
	Write-Output $script | Add-Content $PROFILE
}

"  - Adding fuck() function to current session..."
$env:PYTHONIOENCODING='utf-8'
iex "$($(thefuck --alias).Replace("function fuck", "function global:fuck"))"

"  - Invoking fuck()`n"
fuck @args;
[Console]::ResetColor()
