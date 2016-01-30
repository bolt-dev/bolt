export MOZCONFIG=~/mozconfig.common
export MOZBUILD_STATE_PATH=~/

echo Mach with HOME: ${HOME} PWD: ${PWD} MOZCONFIG: ${MOZCONFIG}
echo Building in TARGET_DIR: ${TARGET_DIR} BUILD_TRIPLE: ${BUILD_TRIPLE}
export PATH=${PATH}:/c/Program\ Files/Git/bin

if [ "$TARGET_NAME" == "xulrunner" ]
then
  cd ~/../comm/mozilla
else
  cd ~/../comm/
fi

echo "${MOCHA_SCRIPT}" in $PWD
eval ${MOCHA_SCRIPT}
exit
