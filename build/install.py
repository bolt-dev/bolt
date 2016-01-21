from __future__ import print_function, unicode_literals

import argparse
import copy
import os
import json
import subprocess
import sys


from BoltUtils import run, checkoutGit, isAppveyor, delDir, delFile, rename, Unbuffered, DropBuffer

dropBuffer = DropBuffer(sys.stdout)
sys.stdout = Unbuffered(sys.stdout)
srcDir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(srcDir)

buildConfig = {}

with open(os.path.join(srcDir, 'build-config.json')) as jsonFile:
  buildConfig = json.load(jsonFile)

def checkoutAll(finished=False):
  for repo in buildConfig['repos']:
    print('Checkout with:' + str(repo))
    uri = repo['uri']
    repoDir = repo['dir']
    branch = repo['branch']
    revision = repo['revision']
    targetDir = os.path.join(srcDir, repoDir)
    if isAppveyor():
      archivePath = '-'.join(repoDir.split('/')) + '.zip'
      if not os.path.exists(archivePath):
        fullURI = 'https://codeload.github.com/%s/zip' % (uri)
        cmd = 'curl -o %s %s/%s' % (archivePath, fullURI, revision)
        if run(cmd.split(' '), cwd=srcDir, stdout=subprocess.PIPE, stderr=subprocess.PIPE).returncode != 0:
          delFile(archivePath)
          return
        # Extract the downloaded file
      delDir(targetDir)
      extracDir = os.path.join(srcDir, repoDir.split('/')[-1] + '-' + revision)
      delDir(extracDir)
      cmd = '7z x %s' % (archivePath)
      if run(cmd.split(' '), cwd=srcDir, stdout=subprocess.PIPE).returncode != 0:
        delFile(archivePath)
        return
      print('Rename %s to %s' % (extracDir, targetDir))
      rename(extracDir, targetDir, True)
    else:
      checkoutGit('https://github.com/%s' % (uri), targetDir, branch, revision=revision)
  return

def install():
  checkoutAll()

if __name__ == '__main__':
  run(['git', '--version'])
  install()
