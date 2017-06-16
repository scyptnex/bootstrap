'''
+-------------------------------------------------------------------------+
|                                  xgpg                                   |
|                                                                         |
| Author: Nic H.                                                          |
| Date: 2016-May-02                                                       |
|                                                                         |
| A GPG decryption layer. converts all arguments which it recognises as   |
| GPG files (filename arguments ending in .gpg and .asc) and temporarily  |
| decrypts them. It then executes all its arguments as a command, where   |
| the GPG files are replaced with their decrypted versions. Finally, if   |
| files have changed, re-encrypts the new files and overwrites their      |
| old encrypted version.                                                  |
|                                                                         |
| The recipient for the GPG file is chosen based on which recipients      |
| are in the previous file, so long as we have their public keys          |
|                                                                         |
| Usage:                                                                  |
|     xgpg [OPTIONS] <COMMAND> [ARGS]                                     |
|                                                                         |
| Options:                                                                |
|   -h         Print this help message                                    |
|   -k         Keep decrypted versions (normally they are deleted)        |
|   -l         Decrypt files into the same directory (i.e. not /tmp/xgpg) |
|   -r <user>  Set the recipient for decrypted files (multiple uses)      |
+-------------------------------------------------------------------------+
'''

__doc__ = __doc__.strip()

import getopt
import pipes
import subprocess
import sys
import tempfile
import os
import re

def gpg_recipients(filename):
    call = ["gpg", "--list-only", "--no-default-keyring", "--secret-keyring", "/dev/null", filename]
    r = [s.strip()[1:-1].decode("utf-8") for s in subprocess.check_output(call, stderr=subprocess.STDOUT).strip().split(b"\n")[1::2]]
    if r:
        return r
    call = ["gpg", "--list-packets", "--no-default-keyring", "--secret-keyring", "/dev/null", filename]
    r = [m.group(1) for m in re.finditer(re.compile("keyid[ \t]*([0-9a-fA-F]+)"), subprocess.check_output(call, stderr=subprocess.STDOUT).strip().decode("utf-8"))]
    if r:
        return r
    raise exception("Could not determine the encryption key for " + filename)

def gpg_decrypt(cipherfile, plainfile):
    subprocess.check_call(["gpg", "--batch", "--yes", "-o", plainfile, cipherfile])

def gpg_encrypt(plainfile, cipherfile, recipients, ascii_mode):
    enc_call = ['gpg', "--batch", "--yes", '-e']
    if ascii_mode:
        enc_call += ['-a']
    for r in recipients:
        enc_call += ['-r', r]
    enc_call += ['-o', cipherfile, plainfile]
    subprocess.check_call(enc_call)

class xgpg:
    def __init__(self):
        self.keep = False
        self.working_dir = os.path.join(tempfile.gettempdir(), "xgpg")
        self.recipients = []
        self.command = []

    def parse_cl(self, sys_args):
        self.keep = False
        self.recipients = []
        try:
            opts, args = getopt.getopt(sys_args[1:], "r:hkl", ["help"])
        except getopt.error as msg:
            print(msg)
            print("for help use --help")
            sys.exit(2)
        for o, a in opts:
            if o in ("-h", "--help"):
                print(__doc__)
                sys.exit(0)
            elif o == "-k":
                self.keep = True
            elif o == "-l":
                self.working_dir = None
            elif o == "-r":
                self.recipients.append(a)
        self.command = args

    def get_decrypted_mirror(self, fi):
        if self.working_dir:
            prefix = os.path.basename(fi)[:-4];
            suffix = ""
            if "." in prefix:
                suffix = prefix[prefix.rfind("."):]
                prefix = prefix[0:prefix.rfind(".")]
            if not os.path.exists(self.working_dir):
                os.makedirs(self.working_dir)
            (handle, path) = tempfile.mkstemp(suffix, prefix, self.working_dir)
            os.remove(path) # not sure how to do this elegantly...
            return path
        else:
            return fi[:-4]

    def clean_temp(self):
        try:
            os.rmdir(self.working_dir)
        except OSError as ex:
            pass

    def execute_command(self):
        enc_dec = {}
        for i, a in enumerate(self.command):
            if ( a.endswith(".gpg") or a.endswith(".asc") ) and not os.path.isdir(a):
                enc_dec[a] = self.get_decrypted_mirror(a)
                if len(self.recipients) == 0 and not os.path.exists(a):
                    print("Aborting: New file \"%s\" must have at least one recipient" % a, file=sys.stderr)
                    return

        # Determine recipients and mod-times for the files
        enc_t = {}
        enc_r = {}
        for enc, dec in enc_dec.items():
            recip = [r for r in self.recipients] # duplicate recipient list
            if os.path.exists(enc):
                # List the recipients of the current file and add them to the recip list
                recip = recip + gpg_recipients(enc)
                # Decrypt the current file
                gpg_decrypt(enc, dec)
            else:
                # Create a new file where needed
                subprocess.check_call(["touch", dec])
            enc_r[enc] = recip
            enc_t[enc] = os.path.getmtime(dec)

        # Call the user's command
        subprocess.call([enc_dec[a] if a in enc_dec.keys() else a for a in self.command])

        # re-encrypt the files
        for enc, dec in enc_dec.items():
            if not os.path.exists(dec):
                print(dec, "captured by command", file=sys.stderr)
                continue
            elif os.path.getmtime(dec) > enc_t[enc]:
                print(dec, "changed, re-encrypting for:", " ".join(enc_r[enc]), file=sys.stderr)
                if os.path.exists(enc):
                    os.remove(enc)
                gpg_encrypt(dec, enc, enc_r[enc], enc.endswith("asc"))
            else:
                print(dec, "unchanged, skipping re-encryption", file=sys.stderr)
            if not self.keep:
                os.remove(dec)
        self.clean_temp()

if __name__ == "__main__":
    x = xgpg()
    x.parse_cl(sys.argv)
    x.execute_command()

