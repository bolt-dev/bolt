call %~dp0prepare-hg.bat
cd /d %~dp0..
set "WD=%CD%"
call :resetGit "%WD%\bolt-sdk"
call :resetGit "%WD%\mozilla"
call :resetGit "%WD%\mozilla\ldap"
call :resetGit "%WD%\mozilla\extensions\irc"
call :resetGit "%WD%\mozilla\extensions\inspector"

pause

goto :eof
:resetGit    - GIT_DIR
if not exist "%~1\.git" goto :eof
cd /d %~1
git stash
git reset --hard
goto :eof
