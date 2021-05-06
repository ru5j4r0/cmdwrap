import sys
import os
import stat

def add_ux(file_name):
    mode_old = os.stat(file_name).st_mode
    mode_new = mode_old | stat.S_IXUSR
    os.chmod(file_name, mode_new)

def template(cmd):
    return f"""#!/usr/bin/env python3

import cmdwrap

BASE_CMD = {cmd}

ROUTING = {{
}}

if __name__ == '__main__':
    cmdwrap.main(ROUTING, BASE_CMD)

"""

def create_file(file_name, cmd):
    with open(file_name, 'w') as fd:
        add_ux(file_name)
        src = template(cmd)
        fd.write(src)

def main():
    if (argc := len(sys.argv)) > 1:
        file_name = sys.argv[1]

        if argc > 2:
            cmd = ' '.join(sys.argv[2:])
            cmd = f"'{cmd}'"
        else:
            cmd = None

        create_file(file_name, cmd)

