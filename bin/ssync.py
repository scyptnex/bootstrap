"""
+-------------------------------------------------------------------------+
|                                ssync.py                                 |
|                                                                         |
| Author: nic                                                             |
| Date: 2017-Apr-30                                                       |
|                                                                         |
| synchronise a secure file and its plaintext-version so that making      |
| changes to one will be reflected in the other                           |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import sys
import getopt

class ssync:
    
    def __init__(self, sys_args):
        try:
            opts, args = getopt.getopt(sys_args[1:], "h", ["help"])
        except getopt.error as exc:
            raise Exception(exc)
        for o, a in opts:
            if o in ("-h", "--help"):
                print(__doc__)
                sys.exit(0)
        if len(args) < 1:
            raise Exception("Provide at lease one argument")
        elif len(args) > 2:
            raise Exception("Too many arguments given")

if __name__ == "__main__":
    try:
        ssync(sys.argv)
    except Exception as exc:
        print(exc, file=sys.stderr)
        print("For help, use -h", file=sys.stderr)
        exit(1)
