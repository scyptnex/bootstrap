"""
+-------------------------------------------------------------------------+
|                              filereduce.py                              |
|                                                                         |
| Author: Nic H.                                                          |
| Date: 2016-Oct-28                                                       |
|                                                                         |
| perform transformations on a stream of records (such as the kind        |
| produced by filemap).                                                   |
|                                                                         |
| Usage:                                                                  |
|   > filereduce {--<command> <arg>}                                      |
|   execute, in order, each of the <Command>s, with the argument <args>.  |
|                                                                         |
| Commands:                                                               |
|   --collect <f>:<op>                                                    |
|     where records are equal for all fields except <f> reduce multiple   |
|     records by applying <op> to the entries of <f>, valid <op>s are:    |
|     avg,sum,max,min,cat                                                 |
|   --remove <f>                                                          |
|     remove the field <f> from all records                               |
|   --rename <old>:<new>                                                  |
|     change the name of the <old> field to <new>                         |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import sys
import getopt
import re

def inputer(fil):
    for ln in fil.readlines():
        yield ln[:-1]

def outputer(s):
    for ln in s:
        print ln

class Command:

    registered=[]

    def __init__(self, n, ac):
        self.name=n
        self.argcount=ac
        Command.registered.append(self)

    def option_string(self):
        return self.name + (min(1, self.argcount)*"=")

    def execute_sub(self, pipeline, args):
        raise Exception("You forgot to override this method for " + self.name)

    def execute(self, pipeline, arg):
        if self.argcount < 1:
            return self.execute_sub(pipeline, [])
        else:
            tmp = arg.split(":")
            if len(tmp) < self.argcount:
                raise Exception("Insufficient arguments to " + self.name)
            return self.execute_sub(pipeline, tmp[:self.argcount-1] + [":".join(tmp[self.argcount-1:])])

def numbr(v):
    return [float(val) for val in v]

class Collect(Command):
    def __init__(self):
        Command.__init__(self, "collect", 2)
    def execute_sub(self, pipe, args):
        ptn=re.compile("(.*)" + args[0] + "=([^\t]*)(.*)")
        op = {
                "avg":lambda c,v : c + "=" + str(sum(numbr(v))/len(v)),
                "max":lambda c,v : c + "=" + str(max(numbr(v))),
                "min":lambda c,v : c + "=" + str(min(numbr(v))),
                "ord":lambda c,v : "\t".join([c + str(i) + "=" + x for (i,x) in enumerate(v)]),
                "sum":lambda c,v : c + "=" + str(sum(numbr(v)))
            }[args[1]]
        d={}
        for ln in pipe:
            m = ptn.match(ln)
            k = m.group(1).split("\t") + m.group(3).split("\t")
            k.sort()
            k = "\t".join([f for f in k if f])
            if not d.has_key(k):
                d[k] = []
            d[k].append(m.group(2))
        for (k,v) in d.items():
            out=""
            try:
                out=op(args[0], v)
            except:
                out=""
            yield (k + "\t" + out).strip()

class Remove(Command):
    def __init__(self):
        Command.__init__(self, "remove", 1)
    def execute_sub(self, pipe, args):
        col_rm=args[0]+"="
        for ln in pipe:
            yield "\t".join([c for c in ln.split("\t") if not c.startswith(col_rm)])

class Rename(Command):
    def __init__(self):
        Command.__init__(self, "rename", 2)
    def execute_sub(self, pipe, args):
        col_from = args[0]
        col_to   = args[1]
        for ln in pipe:
            yield "\t".join([c.replace(col_from,col_to,1) if c.startswith(col_from + "=") else c for c in ln.split("\t")])

def filereduce():
    # register the commands
    Collect()
    Remove()
    Rename()
    # run the pipeline
    pipeline=inputer(sys.stdin)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "h", ["help"] + [c.option_string() for c in Command.registered])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    for o, a in opts:
        if o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif o in ["--" + c.name for c in Command.registered]:
            for c in Command.registered:
                if o == "--" + c.name:
                    pipeline = c.execute(pipeline, a)
    outputer(pipeline)

if __name__ == "__main__":
    filereduce()
