"""
+-------------------------------------------------------------------------+
|                               filemap.py                                |
|                                                                         |
| Author: Nic H.                                                          |
| Date: 2016-Oct-28                                                       |
|                                                                         |
| converts a patterned group of files into a stream of records a'la the   |
| map in map-reduce.                                                      |
|                                                                         |
| Usage:                                                                  |
|   > filemap [Options] <Path-template> [<Content-template>]              |
|   Collect the files matching <Path-template> whose lines match          |
|   <Content-template> into a list of records                             |
|                                                                         |
| Templates:                                                              |
|   a template is an exact matching string containing special __<val>__   |
|   sequences, where the matched entry under __<val>__ will make a value  |
|   in the record line.  The Path-template will glob-match files, while   |
|   the Content-template will grep those files for matching lines. The    |
|   special template "____" exists for matches which dont create fields.  |
|                                                                         |
| Example:                                                                |
|   > filemap "./errors/2016-__MONTH__-__DAY______.log" \                 |
|     "__TYPE__ error at line __LINE__"                                   |
|                                                                         |
|     MONTH=03   DAY=24  LINE=12      TYPE=syntax                         |
|     MONTH=03   DAY=24  LINE=14      TYPE=type                           |
|     MONTH=03   DAY=25  LINE=12      TYPE=syntax                         |
|     ...                                                                 |
|                                                                         |
| Options:                                                                |
|   -d <delim>    use <delim> as field delimiter (instead of tab)         |
|   -f <f>=<val>  force all records to have a field <f> with valye <val>  |
|   -h            print this help message                                 |
|   -r            Treat the content-template as regex, escaping as needed |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import sys
import getopt
import re
import glob

def getFields(start, allTemplates):
    p = re.compile("__([^_]*)__")
    for tmp in allTemplates:
        for m in p.finditer(tmp):
            if m.group(1):
                start[m.group(1)] = ""
    return start

def template_to_regex(templ, fields, escape=True):
    ret = templ
    sig = "__"
    if escape:
        ret = re.escape(ret)
        sig = re.escape(sig)
    for k in fields.keys():
        ret = ret.replace(sig + k + sig, "(?P<" + k + ">.*)")
    ret = ret.replace(sig+sig, ".*")
    return re.compile(ret)

def getTemplates(match, fields):
    for f in fields.keys():
        try:
            yield (f,match.group(f))
        except:
            pass

def updateTemplates(match, fields):
    for (f, v) in getTemplates(match, fields):
        fields[f] = v

def outputTemplates(match, fields, delim):
    fl = fields
    if match:
        fl = fields.copy()
        updateTemplates(match, fl)
    print delim.join([ k + "=" + v.replace("\t","    ") for (k,v) in fl.items() if v])

class Matchr:

    def __init__(self):
        self.delim = "\t"
        self.regexContents=False

    def grepFile(self, realPath, fields, contentPatterns):
        if contentPatterns :
            with open(realPath, "r") as fil:
                for ln in fil.readlines():
                    for c in contentPatterns:
                        m = c.match(ln)
                        if m:
                            outputTemplates(m, fields, self.delim)
        else :
            outputTemplates(None, fields, self.delim)
    
    def searchFiles(self, pathTemplate, fields, contents):
        pathGlob = pathTemplate
        for k in fields.keys():
            pathGlob = pathGlob.replace("__" + k + "__", "____")
        while "________" in pathGlob:
            pathGlob = pathGlob.replace("________", "____")
        pathGlob = pathGlob.replace("____", "*")
        pat = template_to_regex(pathTemplate, fields)
        cpat = [template_to_regex(c, fields, not self.regexContents) for c in contents]
        for fi in glob.glob(pathGlob):
            thisDict=fields.copy()
            updateTemplates(pat.match(fi), thisDict)
            self.grepFile(fi, thisDict, cpat)

def filemap():
    forced_fields = {}
    m=Matchr()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:f:hr", [])
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    for o, a in opts:
        if o in ("-d"):
            m.delim=a
        if o in ("-f"):
            spl = a.split("=")
            forced_fields[spl[0]] = "=".join(spl[1:])
        if o in ("-h"):
            print __doc__
            sys.exit(0)
        if o in ("-r"):
            m.regexContents = True

    fields = getFields(forced_fields, args)
    m.searchFiles(args[0], fields, args[1:])

if __name__ == "__main__":
    filemap()


