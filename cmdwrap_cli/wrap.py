import sys
import os
import stat

def add_ux(file_name):
    s = os.stat(file_name).st_mode
    os.chmod(file_name, s | stat.S_IXUSR)

def init(fd, cmd):
    fd.write(
f"""#!/usr/bin/env python3

import cmdwrap

ROUTING = {{
}}

if __name__ == '__main__':
    cmdwrap.wrap(ROUTING{cmd})

"""
    )

def main():
    argc = len(sys.argv)

    if argc == 2 or argc == 3:
        file_name = sys.argv[1]

        if argc == 3:
            cmd = sys.argv[2]
            cmd = f", '{cmd}'"
        else:
            cmd = ''

        with open(file_name, 'w') as fd:
            add_ux(file_name)
            init(fd, cmd)

