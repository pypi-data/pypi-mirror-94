# OP - Object Programming (test_fuzzer.py)
#
# this file is placed in the public domain

"call all methods"

# imports

import inspect
import op
import op.hdl
import os
import sys
import unittest

sys.path.insert(0, os.getcwd())

from op.hdl import Event, Handler
from op.prs import parse_cli
from op.utl import get_exception, mods

# defines

def cb(event):
    "test callback"
    print("yoo")

cfg = parse_cli()
debug = "d" in cfg.opts
exclude = ["poll", "handler", "input", "doconnect", "raw", "start"]
exc = []
result = []
verbose = "v" in cfg.opts

values = op.Object()
values["txt"] = "yoo"
values["key"] = "txt"
values["value"] = op.Object()
values["d"] = {}
values["hdl"] = Handler()
values["event"] = op.hdl.Event({"txt": "thr", "error": "test"})
values["path"] = op.wd
values["channel"] = "#operbot"
values["orig"] = repr(values["hdl"])
values["obj"] = op.Object()
values["d"] = {}
values["value"] = 1
values["pkgnames"] = "op"
values["name"] = "operbot"
values["callback"] = cb
values["e"] = Event()
values["mod"] = op.hdl.cmd
values["mns"] = "irc,udp,rss"
values["sleep"] = 60.0
values["func"] = cb
values["origin"] = "test@shell"
values["perm"] = "USER"
values["permission"] = "USER"
values["text"] = "yoo"
values["server"] = "localhost"
values["nick"] = "bot"
values["rssobj"] = op.Object()
values["o"] = op.Object()
values["handler"] = Handler()

# unittest

class Test_Fuzzer(unittest.TestCase):

    "fuzzer test"

    def test_fuzz(self):
        global exc
        m = mods("op")
        for x in range(cfg.index or 1):
            for mod in m:
                fuzz(mod)
        exc = []

# functions

def get_values(vars):
    "return value of variable"
    args = []
    for k in vars:
        res = op.get(values, k, None)
        if res:
            args.append(res)
    return args

def handle_type(ex):
    "default failed type handler"
    if debug and verbose:
        print(ex)

def fuzz(mod, *args, **kwargs):
    "do the fuzzing"
    for name, o in inspect.getmembers(mod, inspect.isclass):
        if "_" in name:
            continue
        try:
            oo = o()
        except TypeError as ex:
            handle_type(ex)
            continue
        for name, meth in inspect.getmembers(oo):
            if "_" in name or name in exclude:
                continue
            try:
                spec = inspect.getfullargspec(meth)
                args = get_values(spec.args[1:])
            except TypeError as ex:
                handle_type(ex)
                continue
            if debug and verbose:
                print(meth)
            try:
                res = meth(*args, **kwargs)
                if debug:
                    print("%s(%s) -> %s" % (name, ",".join([str(x) for x in args]), res))
            except Exception as ex:
                if debug:
                    print(get_exception())
