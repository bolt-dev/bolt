from __future__ import print_function, unicode_literals

import sys
import argparse
import copy
import os

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
  setEnv(env, 'HOME', os.path.join(srcDir, 'build'))
  buildHome = os.path.join(srcDir, 'build').replace('\\', '/')
  buildHome = buildHome[0].lower() + buildHome[1:]
  setEnv(env, 'BUILD_HOME', buildHome)
  scriptPath = os.path.join(srcDir, 'mozilla-build', 'start-shell.bat')
  run([scriptPath] + sys.argv[1:], env=env)
  pass

def build():
  print('Start build at:' + srcDir)
  if isWin32():
    buildOnWin32()

if __name__ == '__main__':
  build()
