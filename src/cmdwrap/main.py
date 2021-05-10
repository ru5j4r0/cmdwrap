import sys
from subprocess import run
import piest

def _route(d, args):
    head, rest = piest.list.head_rest(args)

    if head in d.keys():
        v, vt = piest.dict.value_type(d, head)

        if vt == str:
            args[0] = v
        elif vt == dict:
            args[1:] = _route(v, rest)
        elif vt == tuple:
            args[0], new_d = v
            args[1:] = _route(new_d, rest)
        elif callable(vt):
            v(*rest)
            sys.exit(0)

    return args

def _get_args_options():
    return piest.list.divide(sys.argv[1:], '--')

def main(routing, cmd = None):
    args, options = _get_args_options()
    args = _route(routing, args)
    args = piest.list.split_flat(args)

    if cmd:
        run([*cmd.split(), *args])
    elif len(args) > 0:
        run([*args])

