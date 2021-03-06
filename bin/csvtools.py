'''
+------------------------------------------------------------------------------+
|                                   csvtools                                   |
|                                                                              |
| Author: Nic H.                                                               |
| Date: 2015-Aug-19                                                            |
|                                                                              |
| Tools for manipulating CSV files.                                            |
|                                                                              |
| Usage:                                                                       |
|     csvtools [options] <command>                                             |
|                                                                              |
| Options:                                                                     |
|     -h          Print this help message                                      |
|     -o <file>   Output to <file> instead of standard output                  |
|                                                                              |
| Commands:                                                                    |
|     canon <file> [-dqe <char>] [-p <policy>] [-n {column}]                   |
|         Convert the input into a canonical-form CSV, where                   |
|             -d <char>   <char> is the input's delimeter (default: ,)         |
|             -e <char>   <char> is the escape character (default: \)          |
|             -n {column} The input has no header row, generate the header row |
|                         from {column} until it runs out, subsequent columns  |
|                         have "col-<idx>" for their index <idx> as header     |
|             -p <policy> Use quote and escape chars according to <policy>     |
|             -q <char>   <char> is the quotation character (default: ")       |
|                                                                              |
|     display <file>                                                           |
|         Pretty print <file> to screen                                        |
|                                                                              |
|     project <file> {column}                                                  |
|         Output a CSV file with the {column} columns of <file>                |
|                                                                              |
|     sort <file> <column>                                                     |
|         Output a CSV file with non-header rows of <file> sorted by <column>  |
|                                                                              |
| Where applicable, "-" is ther special file name for standard input/output.   |
|                                                                              |
+------------------------------------------------------------------------------+
'''

import sys
import getopt

def display(fi):
    print "Display", fi
    print "Not Implemented yet"

def project(fi, *cols):
    print "Project", fi, "with",
    for i, c in enumerate(cols):
        print c,
    print
    print "Not Implemented yet"

def sort(fi, col):
    print "Sort %s by %s" % (fi, col)
    print "Not Implemented yet"

def csvTools(command, args, output):
    if command == "canon":
        #fil = args[0]
        #delim = ","
        #quot = "\""
        #escape = "\\"
        #try:
        #    copts, cargs = getopt.getopt(args[1:], "d:q:e:p:n")
        #except getopt.error, msg:
        #    print msg
        #    print "for help use -h"
        #    sys.exit(2)
        pass
    elif command == "display":
        display(args[0])
    elif command == "project":
        project(args[0], *args[1:])
    elif command == "sort":
        sort(args[0], args[1])
    else:
        print "Unrecognised command", command
        sys.exit(2)


if __name__ == "__main__":
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:")
    except getopt.error, msg:
        print msg
        print "for help use -h"
        sys.exit(2)
    outp = "-"
    for o, a in opts:
        if o == "-h":
            print __doc__
            sys.exit(0)
        elif o == "-o":
            outp = a
    csvTools(args[0], args[1:], outp)
    
