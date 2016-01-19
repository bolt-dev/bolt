@echo off
set "REPO_DIR=%CD%"
::rd /s /q "%REPO_DIR%.git"

cd /d "%REPO_DIR%\"

cd /d "%REPO_DIR%"

copy /Y .hg\git-mapfile .hg\git-mapfile-backup

if not exist "%REPO_DIR%.git" (
  git init --bare "%REPO_DIR%.git"
)

set errorlevel=0
call hg git-cleanup
call hg push %REPO_DIR%.git

if "%GC_OPTIONS%0" EQU "0" (
  set "GC_OPTIONS=--no-prune"
)

@echo on
if not "%errorlevel%" EQU "0" (
  goto :finished
)
cd .hg\git
git gc %GC_OPTIONS%

if "%~1" equ "" goto :finished
git branch -d master
git push --mirror %~1 --force

:finished
cd /d %WD%
