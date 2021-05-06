import sys
from subprocess import run
from itertools import chain

def _head_rest(head = None, *rest):
    return head, list(rest)

def _route(d, args):
    head, rest = _head_rest(*args)

    if head in d.keys():
        v = d[head]
        vt = type(v)

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

def _preproc_args(args):
    return list(chain.from_iterable(map(str.split, args)))

def wrap(routing, cmd = None):
    args = _route(routing, sys.argv[1:])
    args = _preproc_args(args)

    if cmd:
        run([cmd, *args])
    else:
        if len(args) == 0:
            run('true')
        else:
            run([*args])

