@echo off

python build\install.py

:build

:: For example:
:: python build\build.py "--arch=x64" "--variant=Release" "--target=bolt" %*

python build\build.py --target=xulrunner %*

python build\finish.py

pause
