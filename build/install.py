from __future__ import print_function, unicode_literals


import argparse
import copy
import os

from BoltUtils import run, checkoutGit

srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(srcDir)
def checkout(uri, path, branch):
  checkoutGit(uri, os.path.join(srcDir, path), branch)

def checkoutAll(finished=False):
  checkout('https://github.com/bolt-dev/zero', 'zero-test', None)
  return
  #checkout('https://github.com/html-shell/mozbuild', 'mozbuild', None)
  checkout('https://github.com/html-shell/mozilla-build', 'mozilla-build', None)
  checkout('https://github.com/bolt-dev/comm', 'comm', None)
  checkout('https://github.com/bolt-dev/gecko-dev', 'comm/mozilla', None)

def install():
  checkoutAll()

if __name__ == '__main__':
  run(['git', '--version'])
  install()
