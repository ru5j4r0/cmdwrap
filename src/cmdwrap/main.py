import sys
from subprocess import run
from itertools import chain

def _head_rest(head = None, *rest):
    return head, list(rest)

def _value_type(d, key):
    return (v := d[key]), type(v)

def _route(d, args):
    head, rest = _head_rest(*args)

    if head in d.keys():
        v, vt = _value_type(d, head)

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

def _flatten(l):
    c = chain.from_iterable(l)
    return list(c)

def _preproc_args(args):
    splitted_args = map(str.split, args)
    return _flatten(splitted_args)

def main(routing, cmd = None):
    args = _route(routing, sys.argv[1:])
    args = _preproc_args(args)

    if cmd:
        run([*cmd.split(), *args])
    elif len(args) > 0:
        run([*args])

