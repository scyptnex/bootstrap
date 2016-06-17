"""
+-------------------------------------------------------------------------+
|                                ground.py                                |
|                                                                         |
| Author: Nic H.                                                          |
| Date: 2016-Jun-17                                                       |
|                                                                         |
| short for 'grep around', finds a match for the input string and prints  |
| text around it                                                          |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import sys
import getopt

def ground():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
    print str(args)

if __name__ == "__main__":
    ground()
