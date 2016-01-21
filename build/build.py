from __future__ import print_function, unicode_literals

import sys
import argparse
import copy
import os
import json

from BoltUtils import run,setEnv,isWin32, Unbuffered

sys.stdout = Unbuffered(sys.stdout)
srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(srcDir)


parser = argparse.ArgumentParser(description='Building bolt.')

# Other platform have other CPUs
parser.add_argument('--arch', default='x86', help='The CPU architecture, [i686, x86, x86_64] on Win32')
if isWin32():
  parser.add_argument('--variant', default='Release', help='The build variant [Release, Debug, Release+Debug]')
else:
  parser.add_argument('--variant', default='release', help='The build variant [release, debug, release+debug]')

parser.add_argument('--target', default='bolt', help='The build target [bolt, xulrunner]')
parser.add_argument('--vendor', default='pc-mingw32', help='The build vendor [pc-mingw32, pc-linux]')

args = parser.parse_args()

env = os.environ

def build():
  print('Start build at:' + srcDir)
  options = args
  options.variant = args.variant.lower()
  options.target = args.target.lower()
  options.arch = args.arch
  if isWin32():
    print('Buiding on win32')
    is64 = (args.arch != 'x86') and (args.arch != 'i686')
    archBits = '64' if is64 else '32'
    setEnv(env, 'MOZ_MSVCBITS', archBits)
    setEnv(env, 'MOZ_MSVCVERSION', '12')
    setEnv(env, 'MOZ_MSVCYEAR', '2013')
    options.arch = 'x86_64' if is64 else 'i686'
    options.vendor = 'pc-mingw32'
  options.tripleName = '%s-%s' % (options.arch, options.vendor)
  homeDir = os.path.join(srcDir, 'build').replace('\\', '/')
  options.home = homeDir[0].lower() + homeDir[1:]

  buildHome = os.path.join(os.path.dirname(srcDir), 'bolt-building')
  buildHome = buildHome[0].lower() + buildHome[1:]
  buildDirName =  'Obj-%s-%s-%s' % (options.target, options.tripleName, options.variant)
  options.targetDir = os.path.join(buildHome, buildDirName).replace('\\', '/')

  setEnv(env, 'BUILD_VENDOR', options.vendor)
  setEnv(env, 'BUILD_TRIPLE', options.tripleName)
  setEnv(env, 'HOME', options.home)
  setEnv(env, 'BUILD_VARIANT', options.variant)
  setEnv(env, 'TARGET_NAME', options.target)
  setEnv(env, 'TARGET_DIR', options.targetDir)

  jsonText = json.dumps(env.__dict__, indent=2)
  print('The building env info is:' + jsonText)
  if isWin32():
    scriptPath = os.path.join(srcDir, 'mozilla-build', 'start-shell.bat')
    run([scriptPath] + sys.argv[1:], env=env)
  else:
    print('Not support yet')

if __name__ == '__main__':
  build()
