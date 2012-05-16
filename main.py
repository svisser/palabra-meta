import sys

import commands


if __name__ == '__main__':
    n_args = len(sys.argv)
    if n_args <= 1:
        commands.help()
    elif (not sys.argv[1].startswith('__') and sys.argv[1] in dir(commands)):
        cmd = getattr(commands, sys.argv[1])
        cmd(sys.argv[1:])
    else:
        commands.help()
