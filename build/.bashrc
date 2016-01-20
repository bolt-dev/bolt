export MOZCONFIG=~/mozconfig.common
export MOZBUILD_STATE_PATH=~/
echo The MOZCONFIG is ${MOZCONFIG}
echo HOME: ${HOME} BUILD_HOME: ${BUILD_HOME}
cd ~/../comm/
echo Start building in $PWD with MOZ_MSVCBITS:${MOZ_MSVCBITS} 

./mozilla/mach build
exit
