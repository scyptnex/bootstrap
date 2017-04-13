"""
+-------------------------------------------------------------------------+
|                              securedir.py                               |
|                                                                         |
| Author: nic                                                             |
| Date: 2017-Apr-13                                                       |
|                                                                         |
| Decrypt the gpg-encrypted contents of the stated directory (or "." if   |
| no directory is given) and maintain a synchronised decrypted version    |
| where modifications in either version are reflected in the other.       |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import getopt
import os
import sys
import time

class securedir:
    
    def __init__(self, sys_args):
        self.foreground = False
        try:
            opts, args = getopt.getopt(sys_args[1:], "fh", ["help"])
        except getopt.error, msg:
            print msg
            print "for help use --help"
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                print __doc__
                sys.exit(0)
            elif o == "-f":
                self.foreground = True
        if len(args) < 1 :
            self.dir = "."
        else:
            self.dir = args[0]
        self.dir = os.path.realpath(os.path.abspath(self.dir))

        print(self.dir, "-", self.foreground)


if __name__ == "__main__":
    sd = securedir(sys.argv)
    if sd.foreground:
        time.sleep(3)
        print "fore"
    else:
        print "back"

