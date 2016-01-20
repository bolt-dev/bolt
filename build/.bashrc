CONFIG_GUESS=`~/../comm/build/autoconf/config.guess`
echo The current dir is ${PWD}, CONFIG_GUESS result is ${CONFIG_GUESS}
export TARGET_DIR=$BUILD_HOME/Obj-$TARGET_NAME-$CONFIG_GUESS-$BUILD_VARIANT-${BUILD_ARCH}
echo The target dir is ${TARGET_DIR}

export MOZCONFIG=~/mozconfig.common
export MOZBUILD_STATE_PATH=~/
echo The MOZCONFIG is ${MOZCONFIG}
echo HOME: ${HOME} BUILD_HOME: ${BUILD_HOME}
cd ~/../comm/
echo Start building in $PWD

./mozilla/mach build
exit
