call %~dp0prepare-hg.bat
cd /d %~dp0
set "VCS_SCRIPTS=%CD%"
cd /d %~dp0..
set "WD=%CD%"
set PATH=C:\CI-Tools\vcs\Mercurial-2015;%PATH%
call "%WD%\bolt-sdk\mozilla-build\python\python" "%VCS_SCRIPTS%\SyncHgProject.py"
pause