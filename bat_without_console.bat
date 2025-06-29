@echo off
if "%1" == "h" goto begin
mshta vbscript:createobject("wscript.shell").run("""%~nx0"" h",0)(window.close)&&exit
:begin
setlocal EnableDelayedExpansion
:: 写下你的脚本
setlocal DisableDelayedExpansion
