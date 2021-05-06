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

def _split_list(l, v):
    if v in l:
        i = l.index(v)
        return l[:i], l[i+1:]
    else:
        return l, None

def _get_args_options():
    return _split_list(sys.argv[1:], '--')

def _flatten_list(l):
    c = chain.from_iterable(l)
    return list(c)

def _split_flatten(args):
    splitted_args = map(str.split, args)
    return _flatten_list(splitted_args)

def main(routing, cmd = None):
    args, options = _get_args_options()
    args = _route(routing, args)
    args = _split_flatten(args)

    if cmd:
        run([*cmd.split(), *args])
    elif len(args) > 0:
        run([*args])

