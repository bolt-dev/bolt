call %~dp0prepare-hg.bat
set "PATH=%~dp0;%PATH%"
cd /d %~dp0
set "VCS_SCRIPTS=%CD%"
cd /d %~dp0..
set "WD=%CD%"
call python "%VCS_SCRIPTS%\SyncHgProject.py"
pause