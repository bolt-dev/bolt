@echo off
echo EXCHANGE_TEST_PASSWORD: %EXCHANGE_TEST_PASSWORD%

goto :build
python build\install.py

:build

:: For example:
"python build\build.py  "--arch=x64" "--variant=Release" "--target=bolt"
mozilla-build\python\python build\build.py %*

python build\finish.py
pause
