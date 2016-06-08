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
|   -f         Force decryption, even when the decrypted filename exists  |
|   -h         Print this help message                                    |
|   -k         Keep decrypted versions (normally they are deleted)        |
|   -r <user>  Set the recipient for decrypted files (multiple uses)      |
+-------------------------------------------------------------------------+
'''

__doc__ = __doc__.strip()

import getopt
import pipes
import subprocess
import sys
import os

def parse_cl(sys_argv):
    force = False
    keep = False
    recipients = []
    try:
        opts, args = getopt.getopt(sys_argv[1:], "r:fhk", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    for o, a in opts:
        if o == "-f":
            force = True
        elif o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif o == "-k":
            keep = True
        elif o == "-r":
            recipients.append(a)
    return force, keep, recipients, args

def gpg_recipients(filename):
    return map(lambda s : s.strip()[1:-1], subprocess.check_output(["gpg", "--list-only", "--no-default-keyring", "--secret-keyring", "/dev/null", filename], stderr=subprocess.STDOUT).strip().split("\n")[1::2])

def xgpg(force, keep, recipients, args):
    enc_dec = {}
    for i, a in enumerate(args):
        if ( a.endswith(".gpg") or a.endswith(".asc") ) and not os.path.isdir(a):
            enc_dec[a] = a[:-4]
            if os.path.exists(enc_dec[a]):
                if not force:
                    print "Aborting: cannot decrypt %s since %s already exists.  Use -f to force." % (a, enc_dec[a])
                    return
            if len(recipients) == 0 and not os.path.exists(a):
                print "Aborting: New file \"%s\" must have at least one recipient" % a
                return

    # Determine recipients and mod-times for the files
    enc_t = {}
    enc_r = {}
    for enc in enc_dec.keys():
        recip = [r for r in recipients] # duplicate recipient list
        if os.path.exists(enc):
            # List the recipients of the current file and add them to the recip list
            recip = recip + gpg_recipients(enc)
            # Decrypt the current file
            subprocess.check_call(["gpg", "-o", enc_dec[enc], enc])
        else:
            # Create a new file where needed
            subprocess.check_call(["touch", enc_dec[enc]])
        enc_r[enc] = recip
        enc_t[enc] = os.path.getmtime(enc_dec[enc])

    # Call the user's command
    subprocess.call([enc_dec[a] if a in enc_dec.keys() else a for a in args])

    # re-encrypt the files
    for enc, dec in enc_dec.items():
        if not os.path.exists(dec):
            print dec, "captured by command"
            continue
        elif os.path.getmtime(dec) > enc_t[enc]:
            if os.path.exists(enc):
                os.remove(enc)
            enc_call = ['gpg', '-e']
            if enc.endswith("asc"):
                enc_call += ['-a']
            for r in enc_r[enc]:
                enc_call += ['-r', r]
            enc_call += [dec]
            print dec, "changed, re-encrypting:", " ".join(enc_call)
            subprocess.check_call(enc_call)
        else:
            print dec, "unchanged, skipping re-encryption"
        if not keep:
            os.remove(dec)

if __name__ == "__main__":
    f, k, r, a = parse_cl(sys.argv)
    xgpg(f, k, r, a)
