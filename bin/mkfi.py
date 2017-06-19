"""
+------------------------------------------------------------------------+
|                                    mkfi                                |
|                                                                        |
| Author: Nic H.                                                         |
| Date: 2015-Jan-22                                                      |
|                                                                        |
| Creates a file, and intelligently adds initial comment block and       |
| surrounding data depending on the file type. If the file does not have |
| a recognised extension, or no extension, the default is "sh".          |
|                                                                        |
| usage:                                                                 |
|     mkfi [OPTIONS] <file> [-- {header-args}]                           |
|     Create <file> with its options, and a header created from the      |
|     argumens [header-args] passed to prettybox                         |
|                                                                        |
| Options:                                                               |
|     -a "author"      set the author of the file (Nic H.)               |
|     -h --help        Display this help message                         |
|     -x "extension"   Pretend this is the file's extension (sh)         |
+------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import sys
import getopt
import getpass
import os
import stat
import prettybox 
from string import Template

__templates__={

# C/C++ Source Files
"c":(["--doc"], r'''
${BOX}

#include "${HUMAN_NAME}.h"

using namespace std;

//Default Constructor
${HUMAN_NAME}::${HUMAN_NAME}() {
    //TODO implementation
}

//Default Destructor
${HUMAN_NAME}::~${HUMAN_NAME}() {
    //TODO implementation
}

//Stream output
ostream& operator<<(ostream& os, const ${HUMAN_NAME}& obj) {
    return os << "${HUMAN_NAME}@" << &obj;
}
'''),

# C/C++ Header Files
"h":(["--doc"], r'''
${BOX}

#ifndef __${HEADER_NAME}_H__
#define __${HEADER_NAME}_H__

#include <iostream>

class ${HUMAN_NAME} {
public:
    ${HUMAN_NAME}();
    virtual ~${HUMAN_NAME}();
    void dump() const{std::cout << *this;}
//friends
    friend std::ostream& operator<<(std::ostream&, const ${HUMAN_NAME}&);
};

std::ostream& operator<<(std::ostream&, const ${HUMAN_NAME}&);

#endif /* __${HEADER_NAME}_H__ */
'''),

# Java
"java":(["--doc"], r'''
${BOX}

public class ${HUMAN_NAME} {

    public static void main(String[] args){
        System.out.println("Hello World!");
    }

}
'''),

# Python
"py":(["--box"], r'''
"""
${BOX}
"""

__doc__ = __doc__.strip()

import sys
import getopt

class ${HUMAN_NAME}:
    
    def __init__(self, sys_args):
        try:
            opts, args = getopt.getopt(sys_args[1:], "h", ["help"])
        except getopt.error as exc:
            raise Exception(exc)
        for o, a in opts:
            if o in ("-h", "--help"):
                print(__doc__)
                sys.exit(0)
        print(str(args))

if __name__ == "__main__":
    try:
        ${HUMAN_NAME}(sys.argv)
    except Exception as exc:
        print(exc, file=sys.stderr)
        print("for help use --help", file=sys.stderr)
        sys.exit(2)
'''),

# Python pseudo
"py_pseudo":([], r'''
#! /usr/bin/env sh
exec python3 $$(dirname `readlink -f $$0`)/${HUMAN_NAME}.py "$$@"
'''),

# Shell
"sh":(["--shell"], r'''
#! /usr/bin/env bash

${BOX}

set -e
set -u

function usage(){
    grep "^#.*#$$" $$0
}

function errxit(){
    [ $$# -gt 0 ] && echo "Error: $$@" >&2
    echo "Re-run with -h for help" >&2
    exit 1
}

while getopts "h" opt; do
    case $$opt in
        h)
            usage
            exit 0
            ;;
        \?)
            errxit Unrecognised command
            ;;
    esac
done
shift $$(($$OPTIND -1))

echo $$@
'''),

# Tex
"tex":(["--tex"], r'''
${BOX}

\documentclass{article}

\title{${TITLE_NAME}}
\author{${AUTHOR}}
\date{\today}

\begin{document}

\maketitle

Lorem ipsum dolor set amet.

\end{document}
''')
}

def errxit(msg, code):
    print msg
    sys.exit(code)

def writeFile(dirPath, fileName, pretty_args, author, extension):
    # Process filename for its extension/names
    dotIndex = fileName.rfind(".")
    fType = "sh"
    humanName = fileName
    path = os.path.join(dirPath, fileName)
    if (os.path.exists(path)):
        errxit("%s already exists" % path, 1)
    if dotIndex != -1:
        fType = fileName[dotIndex+1:]
        humanName = fileName[:dotIndex]
    elif __templates__.has_key(extension + "_pseudo"):
        # catch pseudo executables early, and make their execution template
        # in this case a known file type was given that did not have an extension
        writeFile(dirPath, fileName + "." + extension, pretty_args, author, "") # write the real mkfi
        extension = extension + "_pseudo"

    if fType in ("hh", "hpp"):
        fType = "h"
    elif fType in ("cc", "cpp"):
        fType = "c"
    if not __templates__.has_key(fType):
        fType = "sh"
    if len(extension) != 0:
        fType = extension
        if not __templates__.has_key(extension):
            print "Unrecognised extension", extension
            sys.exit(1)
    names = ''.join([" %s" % x if x.isupper() else x for x in humanName.replace("-"," ").replace("_"," ")]).split()

    (box_style, templ) = __templates__[fType]
    f = open(path, "w")
    f.write(Template(templ.strip()).substitute(
            HUMAN_NAME=humanName,
            TITLE_NAME=" ".join(names).title(),
            HEADER_NAME="_".join(names).upper(),
            AUTHOR=author,
            BOX=prettybox.prettybox(box_style + ["-w", "75", "-t", fileName, "-a", author] + pretty_args)
        ) + "\n")
    f.close()
    if(fType == "sh" or fType.endswith("_pseudo")):
        os.chmod(path, os.stat(path).st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)

def main():
    sys_args = sys.argv[1:]
    pretty_args=[]
    if "--" in sys_args:
        idx = sys_args.index("--")
        pretty_args = sys_args[idx+1:]
        sys_args = sys_args[:idx]
    try:
        opts, args = getopt.getopt(sys_args, "a:hx:", ["help"])
    except getopt.error, msg:
        errxit(msg + "\nfor help use --help", 2)

    optAuthor = getpass.getuser()
    optExtension = ""
    for o, a in opts:
        if o in ("-h", "--help"):
            errxit(__doc__, 0)
        elif o in ("-a"):
            optAuthor = a
        elif o in ("-x"):
            optExtension = a

    if(len(args) < 1):
        errxit("Please provide a filename\n" + __doc__, 1)

    else:
        dirPath=os.path.dirname(args[0])
        if(not dirPath):
            dirPath="."
        if(os.path.isdir(dirPath)):
            writeFile(dirPath, os.path.basename(args[0]), pretty_args, optAuthor, optExtension)
        else:
            errxit("Non-existant directory %s" % dirPath, 1)

if __name__ == "__main__":
    main()

