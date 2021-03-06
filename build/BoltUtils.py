from __future__ import print_function, unicode_literals

import os
import pickle
import re
import shutil
import sys
import subprocess

class Unbuffered(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        self.stream.write(data)
        self.stream.flush()
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

class DropBuffer(object):
    def __init__(self, stream):
        self.stream = stream
    def write(self, data):
        pass
    def __getattr__(self, attr):
        return getattr(self.stream, attr)

def getGitHeadRevision(path):
    cmd = 'git rev-parse HEAD'
    if not os.path.exists(path):
        return None
    p = run(cmd.split(' '), cwd=path, stdout=subprocess.PIPE)
    if (p.returncode != 0):
        return None
    return p.stdout

def isWin32():
    return os.name == 'nt'

def isAppveyor():
    return 'APPVEYOR' in os.environ

def checkoutForce(uri, path, branch):
    delFile(os.path.join(path, '.git', 'index.lock'))
    cmd = 'git checkout -f --track -B %s remotes/origin/%s --' % (branch, branch)
    return run(cmd.split(' '), cwd=path).returncode

def getSize(start_path = '.'):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(start_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def rename(src, target, force=False):
    try:
      os.rename(src, target)
    except:
      if not force:
        raise

def checkoutGit(uri, path, branch=None, revision=None, autoCRLF=False):
    parentPath = os.path.dirname(path)
    srcGit = os.path.join(path, '.git')
    targetGit = os.path.join(path, 'cache.git')
    if os.path.exists(path):
        print('The folder size for %s is: %d' % (path, getSize(path)))
          
    branch = branch or 'master'
    parentHead = getGitHeadRevision(parentPath)
    currentHead = getGitHeadRevision(path)
    print('Checkout %s in %s\n ParentHead:%s CurrentHead:%s' %(uri, path, parentHead, currentHead))
    if (parentHead == currentHead or currentHead is None):
        delDir(path)
        print('Need clone ' + uri)
        cmd = 'git clone --bare %s %s' % (uri, os.path.join(path, '.git'))
        if run(cmd.split(' '), cwd=parentPath).returncode != 0:
            print('Clone failed!')
            delDir(path)
            return
    cmd = 'git config --local core.autocrlf %s' % (autoCRLF and 'true' or 'false')
    run(cmd.split(' '), cwd=path)
    run('git config --local core.bare false'.split(' '), cwd=path)

    run('git remote set-url origin'.split(' ') + [uri], cwd=path)
    run('git config --local remote.origin.fetch +refs/heads/*:refs/remotes/origin/*'.split(' '), cwd=path)
    run('git fetch --force --all'.split(' '), cwd=path)
    run('git fetch --force --tags'.split(' '), cwd=path)
    if checkoutForce(uri, path, branch) != 0:
        print('Checkout %s failed' % (uri))
    elif revision:
        cmd = 'git reset --hard %s' % (revision)
        run(cmd.split(' '), cwd=path)

def run(args = [], stdout = sys.stdout, stderr=sys.stderr, shell=False, cwd=None, verborse=True, env=None):
    if (isinstance(args , str)):
      args = [args]
    oldCwd = os.getcwd()
    if cwd:
      os.chdir(cwd)
    if verborse:
      print("Running " + ' '.join(args) + ' in ' + os.getcwd() + ' with ' + str(cwd))
    ret = None
    p = subprocess.Popen(args, shell=shell, stdout=stdout, cwd=cwd, env=env)
    if (stdout == subprocess.PIPE or stderr == subprocess.PIPE):
      [out,err] = p.communicate()
      p.stdout = out
      p.stderr = err
    else:
      p.wait()
    if cwd:
      os.chdir(oldCwd)
    return p

def setEnv(env, key, value):
    env[str(key)] = str(value)

def getFileMetaData(filePath):
    stat = os.stat(filePath)
    t = (long(stat.st_mtime), long(stat.st_size))
    return t

def normalizePath(path):
    p = os.path.normpath(os.sep.join(re.split(r'\\|/', path)))
    if p.find(':') == 1 and getOsName() == 'win':
        return p[0].lower() + p[1:]
    return p

def isSameTime(srcPath, targetPath, testSize = True):
    t1 = getFileMetaData(srcPath)
    t2 = getFileMetaData(targetPath)
    if (t1[0] != t2[0]):
        return False
    if (testSize and t1[1] != t2[1]):
        return False
    return True

def copyFile(srcPath, targetPath):
    if os.path.exists(targetPath):
        if (isSameTime(srcPath, targetPath)):
            return
        os.remove(targetPath)
    p = os.path.dirname(targetPath)
    if not os.path.exists(p):
        os.makedirs (p)
    print("Copy %s as %s" % (srcPath, targetPath))
    shutil.copy2(srcPath, targetPath)

def getOsName():
    os_dir = "win"
    if sys.platform.startswith('freebsd'):
        os_dir = 'freebsd'
    elif sys.platform.startswith('linux'):
        os_dir = 'linux'
    elif sys.platform.startswith('win'):
        os_dir = 'win'
    elif sys.platform.startswith('darwin'):
        os_dir = 'darwin'
    return os_dir

def listFiles(dirPath):
    f = []
    for (dirpath, _, filenames) in os.walk(dirPath):
        f.extend([os.path.join(dirpath, name) for name in filenames])
    return f

def loadPickle(picklePath, default=None):
    try:
        f = open(picklePath, 'rb')
        content = pickle.load(f)
        f.close()
        return content
    except:
        return default

def savePickle(picklePath, content):
    f = open(picklePath, 'wb')
    pickle.dump(content, f)
    f.close()

def handleRemoveReadonly(func, path, exc):
    import stat
    import errno
    excvalue = exc[1]
    print('Remove %s failed' % path)
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise

def makeParentDir(path):
  os.makedirs(os.path.dirname(path))

def delDir(dirPath):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath, ignore_errors=False, onerror=handleRemoveReadonly)

def delFile(f):
  if os.path.exists(f):
    os.remove(f);

__CSL = None
def symlink(source, link_name):
    global __CSL
    if __CSL is None:
        import ctypes
        csl = ctypes.windll.kernel32.CreateSymbolicLinkW
        csl.argtypes = (ctypes.c_wchar_p, ctypes.c_wchar_p, ctypes.c_uint32)
        csl.restype = ctypes.c_ubyte
        __CSL = csl
    flags = 0
    if source is not None and os.path.isdir(source):
        flags = 1
    if __CSL(link_name, source, flags) == 0:
        raise ctypes.WinError()

# The relative path always start with '/' and separate with '/'
def purge(dirPath, pattern):
    if not os.path.exists(dirPath):
        return
    for subDir, _ , files in os.walk(dirPath):
        for filePath in files:
            f = os.path.relpath(os.path.join(subDir, filePath), dirPath)
            f = '/' + f.replace('\\', '/');
            if re.search(pattern, f):
                finalPath = os.path.join(dirPath, os.path.normpath(f[1:]))
                print('Remove path:' + finalPath)
                os.remove(finalPath)
