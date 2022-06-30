@echo off

set flat1=%1
set flat2=%2
set flat3=%3
set flat4=%4

call "dist\automate\automate.exe"  %flat1% %flat2% %flat3% %flat4% 
pause