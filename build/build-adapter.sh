export MOZCONFIG=~/mozconfig.common
export MOZBUILD_STATE_PATH=~/

cd ~/../comm/

echo Mach with HOME: ${HOME} PWD:$PWD MOZCONFIG: ${MOZCONFIG}
echo Building in TARGET_DIR: ${TARGET_DIR} BUILD_TRIPLE:$BUILD_TRIPLE
export PATH=/c/Program\ Files/Git/bin:$PATH
echo ${MOCHA_SCRIPT}
eval ${MOCHA_SCRIPT}
exit
