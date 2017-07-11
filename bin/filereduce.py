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
|                                                                         |
|   > filereduce {--<command> <arg>}                                      |
|   execute, in order, each of the <Command>s, with the argument <args>.  |
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

def mstr(f):
    return "%f" % f

class Collect(Command):
    """
    --collect <f>:<op>
    Where records are equal for all fields except <f> reduce multiple
    Records by applying <op> to the entries of <f>, valid <op>s are:
    avg,sum,max,min,ord
    """
    def __init__(self):
        Command.__init__(self, "collect", 2)
    def execute_sub(self, pipe, args):
        ptn=re.compile("(.*)" + args[0] + "=([^\t]*)(.*)")
        op = {
                "avg":lambda c,v : c + "=" + mstr(sum(numbr(v))/len(v)),
                "max":lambda c,v : c + "=" + mstr(max(numbr(v))),
                "min":lambda c,v : c + "=" + mstr(min(numbr(v))),
                "ord":lambda c,v : "\t".join([c + str(i) + "=" + x for (i,x) in enumerate(v)]),
                "sum":lambda c,v : c + "=" + mstr(sum(numbr(v)))
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

class Default(Command):
    """
    --default <f>:<v>
    if a record has no field named <f>, give it one with value <v>
    """
    def __init__(self):
        Command.__init__(self, "default", 2)
    def execute_sub(self, pipe, args):
        for ln in pipe:
            if args[0] + "=" in ln:
                yield ln
            else:
                yield ln + "\t" + args[0] + "=" + args[1]

class Exclude(Command):
    """
    --exclude <col>:<regex>
    exclude rows where the value in field <col> CONTAINS <regex>
    """
    def __init__(self):
        Command.__init__(self, "exclude", 2)
    def execute_sub(self, pipe, args):
        nm =args[0]
        ptn = re.compile(args[1])
        for ln in pipe:
            mtchd=False
            for c in ln.split("\t"):
                if c.startswith(nm + "=") and ptn.search(c, pos=len(nm)+1):
                    mtchd=True
                    break
            if not mtchd:
                yield ln

class Format(Command):
    """
    --format <col>:<form>
    print the <form> formatted version of the data in <col>
    """
    def __init__(self):
        Command.__init__(self, "format", 2)
    def execute_sub(self, pipe, args):
        fmt="%s="+args[1]
        for ln in pipe:
            yield "\t".join([
                fmt%(args[0], float(c[len(args[0])+1:]))
                if c.startswith(args[0] + "=") else c
                for c in ln.split("\t")])

class Remove(Command):
    """
    --remove <f>
    remove the field <f> from all records
    """
    def __init__(self):
        Command.__init__(self, "remove", 1)
    def execute_sub(self, pipe, args):
        col_rm=args[0]+"="
        for ln in pipe:
            yield "\t".join([c for c in ln.split("\t") if not c.startswith(col_rm)])

class Rename(Command):
    """
    --rename <old>:<new>
    change the name of the <old> field to <new>
    """
    def __init__(self):
        Command.__init__(self, "rename", 2)
    def execute_sub(self, pipe, args):
        col_from = args[0]
        col_to   = args[1]
        for ln in pipe:
            yield "\t".join([c.replace(col_from,col_to,1) if c.startswith(col_from + "=") else c for c in ln.split("\t")])

class Scale(Command):
    """
    --scale <col>:<amt>
    numerically scale the value in <col> by <amt>
    """
    def __init__(self):
        Command.__init__(self, "scale", 2)
    def execute_sub(self, pipe, args):
        col_name = args[0]
        factor   = float(args[1])
        for ln in pipe:
            yield "\t".join([col_name + "=" + str(float(c[c.index("=")+1:])*factor) if c.startswith(col_name + "=") else c for c in ln.split("\t")])

class Sorting(Command):
    """
    --sort <column>
    ensure that all rows containing a <column> field
    appear first and in sorted order
    """
    def __init__(self):
        Command.__init__(self, "sort", 1)
    def execute_sub(self, pipe, args):
        ptn=re.compile("(.*)" + args[0] + "=([^\t]*)(.*)")
        containing=[]
        not_containing=[]
        is_numeric=True
        for ln in pipe:
            m = ptn.match(ln)
            if m:
                containing.append([m.group(2), m.group(1).strip() + "\t" + m.group(3).strip()])
                try:
                    float(m.group(2))
                except ValueError:
                    is_numeric=False
            else:
                not_containing.append(ln)
        if is_numeric:
            containing = [[float(c[0])] + c[1:] for c in containing]
        for pr in sorted(containing, key=lambda pair:pair[0]):
            yield (args[0] + "=" + str(pr[0]) + "\t" + pr[1].strip()).strip()
        for ln in not_containing:
            yield ln

class Split(Command):
    """
    --split <old>:<regex>:<first>:<second>
    split the field data (textually) into two separate fields based on
    the given (bracketed) regex pattern
    """
    def __init__(self):
        Command.__init__(self, "split", 4)
    def execute_sub(self, pipe, args):
        col_name = args[0]
        regx = args[1]
        n1 = args[2]
        n2 = args[3]
        p = re.compile(regx)
        if p.groups != 2:
            raise Exception("Split's regex must have two groups: e.g. ([a-z]*)([A-Z]*)")
        for ln in pipe:
            ret = []
            for c in ln.split("\t"):
                if c.startswith(col_name + "="):
                    m = p.match(c[len(col_name)+1:])
                    if m:
                        if n1:
                            ret.append(n1 + "=" + m.group(1))
                        if n2:
                            ret.append(n2 + "=" + m.group(2))
                    else:
                        raise Exception("%s can not match %s in %s" % (regx, c, ln))
                else:
                    ret.append(c)
            yield "\t".join(ret)


class Table(Command):
    """
    --table <x>:<y>:<val>:<name>:<delim>:<default>
    construct a table from the records, coord (<x>,<y>) has value <val>
    and the table itself is named <name> (i.e. that is the value at the
    (0,0) position). The table will have <delim> as delimiter, and if
    there is no value for a coordinate, <default> is used. Both <delim>
    and <default> can be blank
    """
    def __init__(self):
        Command.__init__(self, "table", 6)
    def execute_sub(self, pipe, args):
        if not args[4]:
            args[4] = "\t"
        xs = []
        ys = []
        ptns = [re.compile(".*" + p + "=([^\t]*)") for p in args[:3]]
        d={}
        for ln in pipe:
            mtch = [m.group(1) if m else "" for m in [p.match(ln) for p in ptns]]
            if not mtch[0] or not mtch[1]:
                raise Exception("trying to create a table with incomplete x and y columns")
            if not mtch[0] in xs:
                xs.append(mtch[0])
            if not mtch[1] in ys:
                ys.append(mtch[1])
            d[(mtch[0], mtch[1])] = mtch[2]
        yield args[4].join([args[3]] + xs)
        for y in ys:
            yield args[4].join([y] + [ s if s else args[5] for s in[d[(x,y)] if (x,y) in d.keys() else None for x in xs]])

def clean(stri):
    for i, ln in enumerate(stri.strip().split("\n")):
        print("%s%s"%("  " if i==0 else "    ", ln.strip()))

def filereduce():
    # register the commands
    Collect()
    Default()
    Exclude()
    Format()
    Remove()
    Rename()
    Scale()
    Sorting()
    Split()
    Table()
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
            print("Commands:")
            for i,c in enumerate(Command.registered):
                if i!=0:
                    print
                clean(c.__doc__)
            sys.exit(0)
        elif o in ["--" + c.name for c in Command.registered]:
            for c in Command.registered:
                if o == "--" + c.name:
                    pipeline = c.execute(pipeline, a)
    outputer(pipeline)

if __name__ == "__main__":
    filereduce()
