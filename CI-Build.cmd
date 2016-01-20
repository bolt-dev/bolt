@echo off
echo EXCHANGE_TEST_PASSWORD: %EXCHANGE_TEST_PASSWORD%

if defined APPVEYOR (
  set BUILD_ARCH=%PLATFORM%
  set BUILD_VARIANT=%CONFIGURATION%
)

if not defined TARGET_NAME (
  set TARGET_NAME=bolt
)

if not defined BUILD_ARCH (
  set BUILD_ARCH=x64
)

if not defined BUILD_VARIANT (
  set BUILD_VARIANT=Release
)

::goto :build

if not defined APPVEYOR (
  python build\install.py
)

:build
cd /d %~dp0
set PATH=%CD%\mozilla-build\python;%PATH%
echo The current python path is:
where python
::python build\build.py

if not defined APPVEYOR (
  python build\finish.py
  pause
)