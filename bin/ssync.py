"""
+-------------------------------------------------------------------------+
|                                ssync.py                                 |
|                                                                         |
| Author: nic                                                             |
| Date: 2017-Apr-30                                                       |
|                                                                         |
| synchronise a secure file and its plaintext-version so that making      |
| changes to one will be reflected in the other                           |
|                                                                         |
| Usage:                                                                  |
|   ssync [Options] <encrypted-directory>                                 |
|                                                                         |
|                                                                         |
|                                                                         |
|                                                                         |
|                                                                         |
|                                                                         |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import getopt
import os
import signal
import sys
import tempfile
import time
import xgpg

class ed_pair:

    def __init__(self, enc, dec):
        self.enc = enc
        self.et = os.path.getmtime(enc) if os.path.exists(enc) else -1
        self.dec = dec
        self.dt = os.path.getmtime(dec) if os.path.exists(dec) else -1

    def manage(self):
        print(str(self), xgpg.gpg_recipients(self.enc))

    def encr(self):
        print("Encrypting", self.dec)

    def decr(self):
        print("Decrypting", self.enc)

    def __str__(self):
        return "%s(%s)<->%s(%s)"%(self.enc, time.ctime(self.et), self.dec, time.ctime(self.dt))

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
        if len(args) != 1 or not os.path.isdir(args[0]):
            raise Exception("Choose exactly one directory to decrypt")
        self.pause = 5
        self.enc_dir = os.path.abspath(os.path.normpath(args[0]))
        self.dec_dir = tempfile.mkdtemp(prefix=os.path.basename(self.enc_dir) + "_")
        self.known = {}
        self.going = False
        self.search(self.enc_dir)

    def search(self, p, low=True):
        if os.path.isdir(p):
            for fn in os.listdir(p):
                self.search(os.path.join(p, fn), low)
        elif not low:
            other = os.path.join(self.enc_dir, os.path.relpath(p, self.dec_dir))
            other = os.path.join(os.path.dirname(other), os.path.basename(other))
            if not other + ".asc" in self.known and not other + ".gpg" in self.known:
                self.known[other + ".gpg"] = ed_pair(other + ".gpg", p)
        elif p.endswith(".asc") or p.endswith(".gpg"):
            other = os.path.join(self.dec_dir, os.path.relpath(p, self.enc_dir))
            other = os.path.join(os.path.dirname(other), os.path.basename(other)[:-4])
            if not p in self.known:
                self.known[p] = ed_pair(p, other)

    def synchronise(self):
        for k, v in self.known.items():
            v.manage()

    def watch(self):
        self.going = True
        self.synchronise()
        while self.going:
            for i in range(0,self.pause):
                if self.going:
                    time.sleep(1)
            self.search(self.enc_dir)
            self.search(self.dec_dir, low=False)
            self.synchronise()
        rm_rf(self.dec_dir)

    def sig_handl(self, signal, frame):
        print() # this is so that your "^C" appears on its own line :)
        self.going = False

def rm_rf(p):
    if os.path.isdir(p):
        for fn in os.listdir(p):
            rm_rf(os.path.join(p, fn))
        os.rmdir(p)
    else:
        os.remove(p)
    print("rm:", p)

if __name__ == "__main__":
    try:
        s = ssync(sys.argv)
        signal.signal(signal.SIGINT, s.sig_handl)
        signal.signal(signal.SIGTERM, s.sig_handl)
        s.watch()
    except Exception as exc:
        print(exc, file=sys.stderr)
        print("For help, use -h", file=sys.stderr)
        exit(1)
