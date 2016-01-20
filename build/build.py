from __future__ import print_function, unicode_literals

import sys
import argparse
import copy
import os
import json

from BoltUtils import run,setEnv,isWin32

srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(srcDir)


parser = argparse.ArgumentParser(description='Building bolt.')

# Other platform have other CPUs
parser.add_argument('--arch', default='x86', help='The CPU architecture, [x86, x86_64] on Win32')
if isWin32():
  parser.add_argument('--variant', default='Release', help='The build variant [Release, Debug, Release+Debug]')
else:
  parser.add_argument('--variant', default='release', help='The build variant [release, debug, release+debug]')

parser.add_argument('--target', default='bolt', help='The build target [bolt, xulrunner]')

args = parser.parse_args()

env = os.environ

def buildOnWin32():
  print('Buiding on win32')
  is64 = args.arch != 'x86'
  archBits = '64' if is64 else '32'
  setEnv(env, 'MOZ_MSVCBITS', archBits)
  setEnv(env, 'MOZ_MSVCVERSION', '12')
  setEnv(env, 'MOZ_MSVCYEAR', '2013')
  buildArch = 'x86_64' if is64 else 'x86'
  setEnv(env, 'BUILD_ARCH', buildArch)
  setEnv(env, 'BUILD_VENDOR', 'pc-mingw32')
  homeDir = os.path.join(srcDir, 'build').replace('\\', '/')
  homeDir = homeDir[0].lower() + homeDir[1:]
  setEnv(env, 'HOME', homeDir)

  buildHome = os.path.join(os.path.dirname(srcDir), 'bolt-building').replace('\\', '/')
  buildHome = buildHome[0].lower() + buildHome[1:]
  setEnv(env, 'BUILD_HOME', buildHome)
  jsonText = json.dumps(env.__dict__, indent=2)
  print('The building env info is:' + jsonText)
  scriptPath = os.path.join(srcDir, 'mozilla-build', 'start-shell.bat')
  run([scriptPath] + sys.argv[1:], env=env)

def build():
  print('Start build at:' + srcDir)
  setEnv(env, 'BUILD_VARIANT', args.variant.lower())
  setEnv(env, 'TARGET_NAME', args.target.lower())

  if isWin32():
    buildOnWin32()

if __name__ == '__main__':
  build()
