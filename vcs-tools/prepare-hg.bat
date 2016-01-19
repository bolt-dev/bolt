cd /d %~dp0..\..\bolt-mirror
set WD=%CD%
set "VCS_TOOLS=C:\CI-Tools\vcs"
set PATH=%VCS_TOOLS%\Mercurial;%VCS_TOOLS%\git\cmd;%PATH%
cd /d %WD%
