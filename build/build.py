from __future__ import print_function, unicode_literals

import sys
import argparse
import copy
import os
import json

from BoltUtils import run,setEnv,isWin32

srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(srcDir)

def buildOnWin32():
  print('Buiding on win32')
  env = os.environ
  is64 = 'BUILD_ARCH' in env and env['BUILD_ARCH'] != 'x86'

  arch = '64' if is64 else '32'
  setEnv(env, 'MOZ_MSVCBITS', arch)
  setEnv(env, 'MOZ_MSVCVERSION', '12')
  setEnv(env, 'MOZ_MSVCYEAR', '2013')
  setEnv(env, 'BUILD_VARIANT', env['BUILD_VARIANT'].lower())
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
  if isWin32():
    buildOnWin32()

if __name__ == '__main__':
  build()
