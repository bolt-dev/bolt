import sys
import os
import subprocess
import shutil
import re
import pickle
import time

from datetime import datetime
from datetime import timedelta
from datetime import tzinfo

def handleRemoveReadonly(func, path, exc):
    import stat
    import errno
    excvalue = exc[1]
    if func in (os.rmdir, os.remove) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU| stat.S_IRWXG| stat.S_IRWXO) # 0777
        func(path)
    else:
        raise

def delDir(dirPath):
    if os.path.exists(dirPath):
        shutil.rmtree(dirPath, ignore_errors=True, onerror=handleRemoveReadonly)

os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
srcDir = os.path.normpath(os.getcwd())

mirrorDir = os.path.dirname(srcDir)

def RunHg(args = [], stdout = sys.stdout, stderr=sys.stderr, verborse=True):
    if (isinstance(args , str)):
        args = [args]
    args = ['hg'] + args
    if verborse:
      print("Running " + ' '.join(args) + ' in ' + os.getcwd())
    hg = subprocess.Popen(args, shell = False, stdout=stdout, stderr=stderr)
    if stdout == subprocess.PIPE or stderr == subprocess.PIPE:
        ret = hg.communicate()
        if verborse:
          print('Running finished')
        return hg.returncode, ret
    return hg.wait()

def RunGitConvert(args = [], stdout = sys.stdout, stderr=sys.stderr, verborse=True):
    if (isinstance(args , str)):
        args = [args]
    args = ['git-convert'] + args
    if verborse:
      print("Running " + ' '.join(args) + ' in ' + os.getcwd())
    git = subprocess.Popen(args, shell = True, stdout=stdout, stderr=stderr)
    if stdout == subprocess.PIPE or stderr == subprocess.PIPE:
        ret = git.communicate()
        if verborse:
          print('Running finished')
        return git.returncode, ret
    return git.wait()

def CloneURL(dirPath, url, repoName, force = False):
    try:
        if not os.path.exists(dirPath):
            os.makedirs(dirPath)
        repoPath = os.path.join(dirPath, repoName)
        if force:
            delDir(repoPath)
        if os.path.exists(repoPath):
            return -1
    except Exception as e:
        print(e)
        return -1
    os.chdir(dirPath)

    ret = RunHg(['clone', '-U', url, repoName])
    if ret > 0:
        return ret
    os.chdir(os.path.join(dirPath, repoName))
    #RunHg(['update', 'null'])

def Pull(dirPath, url, repoName, branchName):
    repoPath = os.path.join(dirPath, repoName)
    repoHgPath = os.path.join(repoPath, '.hg')
    ret = 0
    if not os.path.exists(repoHgPath):
        ret = CloneURL(dirPath, url, repoName, True)
    if ret > 0 or not os.path.exists(repoHgPath):
        return -1
    os.chdir(repoPath)
    return RunHg(['pull', url])

CHATZILLA_REPO_LIST = [
    ('https://hg.mozilla.org/chatzilla', 'default'),
]

DOM_INSPECTOR_REPO_LIST = [
    ('https://hg.mozilla.org/dom-inspector', 'default'),
]

COMM_REPO_LIST = [
    ('http://hg.mozilla.org/comm-central', 'default'),
    ('http://hg.mozilla.org/releases/comm-aurora', 'aurora'),
    ('http://hg.mozilla.org/releases/comm-beta','beta'),
    ('http://hg.mozilla.org/releases/comm-release', 'release'),
    ('http://hg.mozilla.org/releases/comm-esr38', 'esr38'),
    ('http://hg.mozilla.org/releases/comm-esr31', 'esr31'),
    ('http://hg.mozilla.org/releases/comm-esr24', 'esr24'),
    ('http://hg.mozilla.org/releases/comm-esr17', 'esr17'),
    ('http://hg.mozilla.org/releases/comm-esr10', 'esr10'),
    #('https://reviewboard-hg.mozilla.org/comm-central', 'reviewboard'),
]

MOZILLA_REPO_LIST = [
    ('http://hg.mozilla.org/mozilla-central', 'default'),
    ('https://hg.mozilla.org/projects/larch', 'larch'),
    ('http://hg.mozilla.org/integration/mozilla-inbound', 'inbound'),
    ('http://hg.mozilla.org/integration/b2g-inbound', 'b2g-inbound'),
    ('http://hg.mozilla.org/integration/fx-team', 'fx-team'),
    ('http://hg.mozilla.org/releases/mozilla-aurora', 'aurora'),
    ('http://hg.mozilla.org/releases/mozilla-beta', 'beta'),
    ('http://hg.mozilla.org/releases/mozilla-release', 'release'),
    ('http://hg.mozilla.org/releases/mozilla-esr38', 'esr38'),
    ('http://hg.mozilla.org/releases/mozilla-b2g32_v2_0m', 'b2g32_v2_0m'),
    ('http://hg.mozilla.org/releases/mozilla-b2g32_v2_0', 'b2g32_v2_0'),
    ('http://hg.mozilla.org/releases/mozilla-b2g34_v2_1', 'b2g34_v2_1'),
    ('http://hg.mozilla.org/releases/mozilla-esr31', 'esr31'),
    ('http://hg.mozilla.org/releases/mozilla-b2g30_v1_4', 'b2g30_v1_4'),
    ('http://hg.mozilla.org/releases/mozilla-b2g28_v1_3t', 'b2g28_v1_3t'),
    ('http://hg.mozilla.org/releases/mozilla-b2g28_v1_3', 'b2g28_v1_3'),
    ('http://hg.mozilla.org/releases/mozilla-b2g26_v1_2f', 'b2g26_v1_2f'),
    ('http://hg.mozilla.org/releases/mozilla-b2g26_v1_2', 'b2g26_v1_2'),
    ('http://hg.mozilla.org/releases/mozilla-esr24', 'esr24'),
    ('http://hg.mozilla.org/releases/mozilla-b2g18', 'b2g18'),
    ('http://hg.mozilla.org/releases/mozilla-b2g18_v1_1_0_hd', 'b2g18_v1_1_0_hd'),
    ('http://hg.mozilla.org/releases/mozilla-b2g18_v1_1_0', 'b2g18_v1_1_0'),
    ('http://hg.mozilla.org/releases/mozilla-b2g18_v1_0_1', 'b2g18_v1_0_1'),
    ('http://hg.mozilla.org/releases/mozilla-b2g18_v1_0_0', 'b2g18_v1_0_0'),
    ('http://hg.mozilla.org/releases/mozilla-esr17', 'esr17'),
    ('http://hg.mozilla.org/releases/mozilla-esr10', 'esr10'),
    ('http://hg.mozilla.org/releases/mozilla-2.1', '2.1'),
    ('http://hg.mozilla.org/releases/mozilla-2.0', '2.0'),
    ('http://hg.mozilla.org/releases/mozilla-1.9.2', '1.9.2'),
    ('http://hg.mozilla.org/releases/mozilla-1.9.1', '1.9.1'),
    ('http://hg.mozilla.org/releases/mozilla-mobile-6.0', 'mobile-6.0'),
    ('http://hg.mozilla.org/releases/mozilla-mobile-5.0', 'mobile-5.0'),
    #('https://reviewboard-hg.mozilla.org/gecko', 'reviewboard'),
]

def PullRepoList(repoList, repoName):
    ret = 0
    for repoConfig in repoList:
        ret = ret or Pull(mirrorDir, repoConfig[0], repoName, repoConfig[1])
    return ret

def FilterBranchesResult(branchNames, isURL):
    finalBranchNames = []
    for branchName in branchNames:
        print(branchName)
        splitBranchName = filter(None, re.split("[\* \n:]+", branchName))
        if len(splitBranchName) > 1:
            if isURL:
                finalBranchNames.append(splitBranchName)
            else:
                finalBranchNames.append([splitBranchName[0],splitBranchName[2]])
    finalBranchNames.sort()
    return finalBranchNames

def GetBranchRevision(url, branchName):
    if branchName:
        url = url + '#' + branchName
    print("Query " + url + "'s identify")
    errorCode, hg = RunHg(['identify', '--id', url], stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    return errorCode, hg[0].split('\n')[0]

class FixedOffset(tzinfo):
    """Fixed offset in minutes east from UTC."""

    def __init__(self, dt, name=None):
        self.__offset = dt
        self.__name = name

    def utcoffset(self, dt):
        return self.__offset

    def tzname(self, dt):
        return self.__name

    def dst(self, dt):
        return timedelta(0)

def GetAllBranches(args = ['branches', '-c'], repoPath=None, isURL = False):
    print("The command is " + ' '.join(args))
    if repoPath:
        os.chdir(repoPath)
    errorCode, hg = RunHg(args, stdout = subprocess.PIPE)
    if (errorCode != 0):
        return errorCode, []
    return 0, FilterBranchesResult(hg[0].split('\n'), isURL)

def SyncHgBookmark(repoList, repoName, gitPushURI):
    repoPath = os.path.join(mirrorDir, repoName)
    errorCode = PullRepoList(repoList, repoName)
    if errorCode !=0:
        return errorCode
    errorCode, allBranches = GetAllBranches(repoPath = repoPath)
    if errorCode != 0:
        return errorCode
    repoHgPath = os.path.join(repoPath, '.hg')
    if not os.path.exists(repoHgPath):
      return -1
    revisionMap = {}
    revisionOrder = []
    branchesInfo = {}
    dateMap = {}
    revisionDate = {}
    revisionDatePath = os.path.join(repoHgPath, 'revision-date.cache')
    try:
      revisionDate = pickle.load(open(revisionDatePath, 'rb'))
    except:
      pass

    for url,branchName in repoList:
        errorCode,branches = GetAllBranches(args=['identify', '-l', url], repoPath=mirrorDir, isURL=True)
        if errorCode != 0:
            return errorCode

        for branch in branches:
            name = branch[0]
            revisions = branch[1:]
            if (not name in branchesInfo):
                branchesInfo[name] = set()
            os.chdir(repoHgPath)
            for r in revisions:
              hg = None
              if r in revisionDate:
                hg = revisionDate[r]
              else:
                errorCode, hg = RunHg(['log', '--template', '{date|hgdate}', '-r', r], stdout = subprocess.PIPE, verborse=False)
                if errorCode != 0:
                  continue
                revisionDate[r] = hg
              if r in dateMap:
                continue
              dateMap[r] = None
              try:
                timestamp_str, timezone_str = hg[0].split(' ')
                dt = timedelta(seconds=int(timezone_str))
                finalTime = datetime.fromtimestamp(int(timestamp_str), FixedOffset(dt))
                ts = finalTime.utctimetuple()
                t = time.mktime(ts)
                dateMap[r] = t
              except Exception as e:
                print(e)
            sortedRevisions = sorted(revisions, key = lambda r:dateMap[r], reverse = True)
            for r in sortedRevisions:
                if dateMap[r] is None:
                  continue
                if r in branchesInfo[name]:
                    continue
                if not r in revisionMap:
                    revisionMap[r] = []
                    revisionOrder.append(r)
                revisionMap[r].append((name, branchName))
            branchesInfo[name] |= set(revisions)

    pickle.dump(revisionDate, open(revisionDatePath, "wb"))
    bookmarkMap = {}
    for r in revisionOrder:
        for name, branchName in revisionMap[r]:
            targetName = name if name != 'default' else branchName
            if targetName in bookmarkMap:
                if targetName == 'reviewboard':
                    continue
                if (bookmarkMap[targetName] == r):
                    continue
                if targetName != branchName:
                    targetName = targetName + '_' + branchName
            if targetName in bookmarkMap:
                if (bookmarkMap[targetName] == r):
                    continue
                targetName = targetName + '_' + r
            print("%s %s %s %s" %(name, branchName, targetName, r))
            bookmarkMap[targetName] = r

    for name, revision in allBranches:
        if not name in bookmarkMap:
            print("Can not found branch:" + name)
            return -1

    errorCode, allBookmarks = GetAllBranches(args=['bookmarks'], repoPath = repoPath)
    allBookmarks = dict(allBookmarks)
    revisionCount = {}
    for name,revision in bookmarkMap.iteritems():
        if revision in revisionCount:
            revisionCount[revision] = revisionCount[revision] + 1
            print("Multiple branch point to the same revision " + revision)
        else:
            revisionCount[revision] = 1
        if (name in allBookmarks) and revision == allBookmarks[name]:
            print("Exist bookmark %s as revision %s." % (name,revision))
            continue
        print("Setting bookmark %s to revision %s." % (name,revision))
        errorCode = RunHg(['bookmark', '-f', '--rev', revision, name])
        if errorCode != 0:
            return errorCode

    for name, revision in allBookmarks.iteritems():
        if not name in bookmarkMap:
            print("The bookmark %s should be removed" % name)
            errorCode = RunHg(['bookmark', '-f', '-d', name])
            if errorCode != 0:
                #return errorCode
                pass

    os.chdir(repoPath)
    return RunGitConvert([gitPushURI])

locales = [
  'ach',
  'af',
  'ak',
  'ar',
  'as',
  'ast',
  'be',
  'bg',
  'bn-BD',
  'bn-IN',
  'br',
  'bs',
  'ca',
  'cs',
  'cy',
  'da',
  'de',
  'el',
  'en-GB',
  'en-ZA',
  'eo',
  'es-AR',
  'es-CL',
  'es-ES',
  'es-MX',
  'et',
  'eu',
  'fa',
  'ff',
  'fi',
  'fr',
  'fy-NL',
  'ga-IE',
  'gd',
  'gl',
  'gu-IN',
  'he',
  'hi-IN',
  'hr',
  'hu',
  'hy-AM',
  'id',
  'is',
  'it',
  'ja',
  'ja-JP-mac',
  'ka',
  'kk',
  'km',
  'kn',
  'ko',
  'ku',
  'lg',
  'lij',
  'lt',
  'lv',
  'mai',
  'mk',
  'ml',
  'mn',
  'mr',
  'ms',
  'my',
  'nb-NO',
  'ne-NP',
  'nl',
  'nn-NO',
  'nr',
  'nso',
  'oc',
  'or',
  'pa-IN',
  'pl',
  'pt-BR',
  'pt-PT',
  'rm',
  'ro',
  'ru',
  'rw',
  'si',
  'sk',
  'sl',
  'son',
  'sq',
  'sr',
  'ss',
  'st',
  'sv-SE',
  'ta',
  'ta-LK',
  'te',
  'th',
  'tn',
  'tr',
  'ts',
  'uk',
  've',
  'vi',
  'wo',
  'x-testing',
  'xh',
  'zh-CN',
  'zh-TW',
  'zu'
]

# https://hg.mozilla.org/releases/l10n/mozilla-release
def main(argv):
    RunHg('--version')
    for name in locales:
      l10n = [
        ('https://hg.mozilla.org/l10n-central/' + name, 'default'),
        ('https://hg.mozilla.org/releases/l10n/mozilla-release/' + name, 'release')
      ]
      SyncHgBookmark(l10n, 'l10n/' + name, 'git@github.com:mail-apps-l10n/' + name + '.git')
    SyncHgBookmark(CHATZILLA_REPO_LIST, 'chatzilla', 'git@github.com:mail-apps/chatzilla.git')
    SyncHgBookmark(DOM_INSPECTOR_REPO_LIST, 'dom-inspector', 'git@github.com:mail-apps/inspector.git')
    SyncHgBookmark(COMM_REPO_LIST, 'comm', 'git@github.com:mail-apps/comm.git')
    SyncHgBookmark(MOZILLA_REPO_LIST, 'mozilla', 'git@github.com:mail-apps/gecko-dev.git')
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
