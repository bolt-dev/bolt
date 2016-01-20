from __future__ import print_function, unicode_literals


import argparse
import copy
import os

from BoltUtils import run, checkoutGit

srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(srcDir)
isFinish = False
def checkout(uri, path, branch):
  global isFinish
  checkoutGit(uri, os.path.join(srcDir, path), branch, isFinish)

def checkoutAll(finished=False):
  global isFinish
  isFinish = finished
  print('The src dir is: ' + srcDir)
  checkout('https://github.com/html-shell/mozbuild', 'mozbuild', None)

  # Try the git clone done properly first
  checkout('https://github.com/html-shell/mozilla-build', 'mozilla-build', None)
  checkout('https://github.com/bolt-dev/comm', 'comm', None)
  print("checkout mozbuild first")
  return 
  checkout('https://github.com/bolt-dev/gecko-dev', 'comm/mozilla', None)

def install():
  checkoutAll()

if __name__ == '__main__':
  run(['git', '--version'])
  install()
