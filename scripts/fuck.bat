@set PYTHONIOENCODING=utf-8
@powershell -noprofile -c "cmd /c \"$(thefuck %* $(doskey /history)[-2])\"; [Console]::ResetColor();"
