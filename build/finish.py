from __future__ import print_function, unicode_literals
import sys
from BoltUtils import Unbuffered

sys.stdout = Unbuffered(sys.stdout)

if __name__ == '__main__':
  print('Running the finish script')
