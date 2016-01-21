export MOZCONFIG=~/mozconfig.common
export MOZBUILD_STATE_PATH=~/

cd ~/../comm/

echo Mach with HOME: ${HOME} PWD:$PWD
echo TARGET_DIR: ${TARGET_DIR} BUILD_TRIPLE:$BUILD_TRIPLE
echo MOZCONFIG: ${MOZCONFIG}

./mozilla/mach build
exit
