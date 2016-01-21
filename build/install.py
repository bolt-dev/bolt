from __future__ import print_function, unicode_literals


import argparse
import copy
import os

from BoltUtils import run, checkoutGit, isAppveyor

srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(srcDir)
def checkout(uri, path, branch):
  checkoutGit(uri, os.path.join(srcDir, path), branch)

def checkoutAll(finished=False):
  #checkout('https://github.com/bolt-dev/zero', 'mozbuild', None)
  checkout('https://github.com/html-shell/mozbuild', 'mozbuild', None)
  checkout('https://github.com/html-shell/mozilla-build', 'mozilla-build', None)
  checkout('https://github.com/bolt-dev/comm', 'comm', None)

  if isAppveyor():
    uri = 'https://codeload.github.com/bolt-dev/gecko-dev/tar.gz'
    revision = '0c2a880ad0964532ec47c6af19d8ac6ede2c140c'
    cmd = 'curl -o gecko-dev.tar.gz %s/%s' % (uri, revision)
    run(cmd.split(' '))
  else:
    checkout('https://github.com/bolt-dev/gecko-dev', 'comm/mozilla', None)

def install():
  checkoutAll()

if __name__ == '__main__':
  run(['git', '--version'])
  install()
