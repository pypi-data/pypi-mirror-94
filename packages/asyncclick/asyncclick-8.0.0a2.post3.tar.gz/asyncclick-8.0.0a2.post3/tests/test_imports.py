import json
import subprocess
import sys

from asyncclick._compat import WIN


IMPORT_TEST = b"""\
import builtins

found_imports = set()
real_import = builtins.__import__
import sys

def tracking_import(module, locals=None, globals=None, fromlist=None,
                    level=0):
    rv = real_import(module, locals, globals, fromlist, level)
    if globals and globals['__name__'].startswith('click') and level == 0:
        found_imports.add(module)
    return rv
builtins.__import__ = tracking_import

import asyncclick as click
rv = list(found_imports)
import json
click.echo(json.dumps(rv))
"""

ALLOWED_IMPORTS = {
    "weakref",
    "os",
    "struct",
    "collections",
    "sys",
    "contextlib",
    "functools",
    "stat",
    "re",
    "codecs",
    "inspect",
    "itertools",
    "io",
    "threading",
    "colorama",
    "errno",
    "fcntl",
    "datetime",
    "enum",
}

if WIN:
    ALLOWED_IMPORTS.update(["ctypes", "ctypes.wintypes", "msvcrt", "time", "zlib"])


def test_light_imports():
    c = subprocess.Popen(
        [sys.executable, "-"], stdin=subprocess.PIPE, stdout=subprocess.PIPE
    )
    rv = c.communicate(IMPORT_TEST)[0]
    rv = rv.decode("utf-8")
    imported = json.loads(rv)

    for module in imported:
        if module == "asyncclick" or module.startswith("asyncclick."):
            continue
        assert module in ALLOWED_IMPORTS
