"""
+-------------------------------------------------------------------------+
|                               tabulate.py                               |
|                                                                         |
| Author: Nic H.                                                          |
| Date: 2016-Oct-27                                                       |
|                                                                         |
| Tabulate information from multiple files into a CSV file, and print the |
| output in a pretty table format.                                        |
|                                                                         |
| Usage:                                                                  |
|   tabulate [OPTIONS] <TEMPLATE> {PATTERN}                               |
|                                                                         |
| Template:                                                               |
|   The pattern string which is matched to locate different test cases    |
|   The following keywords can only appear in the template:               |
|   XXX        Each different value here creates a different X coord      |
|   YYY        Each different value here creates a different Y coord      |
|                                                                         |
| Pattern:                                                                |
|   The pattern string which is matched to find relevant lines in each    |
|   test case's file.                                                     |
|   AVG        X/Y values are the average of items found here             |
|   MIN        X/Y values are the minimum amongst items found here        |
|   MAX        X/Y values are the maximum amongst items found here        |
|   SUM        X/Y values are the sum of items found here                 |
|   NUM        X/Y values are the count of items found here               |
|                                                                         |
| Options:                                                                |
|   -h         Display this help message                                  |
|                                                                         |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import getopt
import glob
import re
import sys

keywords=["XXX", "YYY", "AVG", "MIN", "MAX", "SUM", "NUM"]

def template_to_regex(templ):
    """ return a compiled regex pattern with the correct groups to match this string """
    regexStr = re.escape(templ)
    for kw in keywords:
        count=0
        while kw in regexStr:
            regexStr = regexStr.replace(kw, "(?P<" + kw[:-1] + str(count) + ">.*)")
            count += 1
    return re.compile(regexStr)

class Tabl:

    def __init__(self, templ, patts):
        self.template = templ
        self.patterns = patts
        self.files = []
        self.xs = []
        self.ys = []
        self.execute()

    def execute(self):
        self.search()

    def search(self):
        # get the files
        globStr = self.template
        for kw in keywords:
            globStr = globStr.replace(kw, "*")
        self.files = glob.glob(globStr)
        # find the x/ys
        pattern = template_to_regex(self.template)
        for fi in self.files:
            m = re.match(pattern, fi)
            print m.group("YY0")
        


def tabulate():
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
    if len(args) < 1:
        print "please provide the template pattern"
        sys.exit(1)
    t = Tabl(args[0], args[1:])


if __name__ == "__main__":
    tabulate()
