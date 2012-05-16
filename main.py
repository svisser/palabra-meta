import sys

from commands import initialimport


if len(sys.argv) > 1:
    if sys.argv[1] == 'initialimport':
        initialimport.run()
