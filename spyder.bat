@echo off
setlocal
REM set PATH=c:\windows\systems32;c:\anaconda2;c:\anaconda2\Library\usr\bin;c:\anaconda2\Library\bin;c:\anaconda2\Scripts;%PATH%
REM c:\anaconda2\python.exe c:\anaconda2\Scripts\spyder-script.py
set PATH=%SystemRoot%\system32;%SystemRoot%;%SystemRoot%\System32\Wbem;c:\anaconda3-b4;c:\anaconda3-b4\Library\usr\bin;c:\anaconda3-b4\Library\bin;c:\anaconda3-b4\Scripts;%PATH%

c:\anaconda3-b4\python.exe c:\anaconda3-b4\Scripts\spyder-script.py
endlocal
