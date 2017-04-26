'''
+-----------------------------------------------------------------------+ 
|                               prettybox                               |
|                                                                       |
| Author: Nic H.                                                        |
| Date: 2016-Apr-07                                                     |
|                                                                       |
| Wraps the specified text in a pretty box-shape as specified by the    |
| user. Works both for large boxes and small headers. Users choose from |
| a list of pre-fabricated styles, or design their own. Pre-fabricated  |
| styles beginning with "u" indicate unicode.                           |
|                                                                       |
| Usage:                                                                |
|     prettybox [OPTIONS] [--STYLE] [--PIECE=CHAR] {MESSAGE}            |
|                                                                       |
| OPTIONS:                                                              |
|   -a NAME     Name of the author field                                |
|   -b          Force big mode, i.e. draw a big box with no title       |
|   -h          print this help message                                 |
|   -o O:A:MSG  Append a big box.s message with an option-style line of |
|               the form .-O A MSG.                                     |
|   -t TITLE    Set the title of the box, it will be centered and big-  |
|               mode will be enabled                                    |
|   -w WIDTH    Set the width of the box                                |
|                                                                       |
| STYLE:                                                                |
|     box, block, doc, inline, plain, shell, tex, ucurve, udouble,      |
|     uthick                                                            |
|                                                                       |
| PIECES:                                                               |
|     N, NE, E, SE, S, SW, W, NW                                        |
|     The compass directions are strings used to draw the box           |
+-----------------------------------------------------------------------+
'''

__doc__ = __doc__.strip()

import datetime
import getopt
import getpass
import sys
import textwrap

def toWidthString(stri, width, left, right, centered):
    if not left:
        stri = stri.lstrip()
    spc=width-len(stri + left + right)
    if(spc < 0):
        raise Exception("Not enough space for line \"%s\" %d" % (stri, spc))
    ret = stri + " "*spc + right
    if(centered):
        ret = " "*(spc//2) + stri + " "*(spc - spc//2) + right
    return left + ret.rstrip()

def boxerize(p, m, w=-1, t="", a="", d="", o=[]):
    ret = []
    if w==-1:
        w = 2+len(p["W"] + m + p["E"])
    if p["NW"]:
        ret.append(p["NW"] + (w-len(p["NW"] + p["NE"]))*p["N"] + p["NE"])
    if t:
        ret.append(toWidthString(t, w, p["W"], p["E"], True))
        ret.append(toWidthString("", w, p["W"], p["E"], False))
    if a:
        ret.append(toWidthString(" Author: " + a, w, p["W"], p["E"], False))
    if d:
        ret.append(toWidthString(" Date: " + d, w, p["W"], p["E"], False))
    if m:
        if a or d:
            ret.append(toWidthString("", w, p["W"], p["E"], False))
        wrapper = textwrap.TextWrapper()
        wrapper.width = w - len(p["W"] + p["E"]) - 2
        for line in wrapper.wrap(m):
            ret.append(toWidthString(" " + line, w, p["W"], p["E"], False))
    if o:
        if a or d or m:
            ret.append(toWidthString("", w, p["W"], p["E"], False))
        wrapper = textwrap.TextWrapper()
        ret.append(toWidthString(" Options:", w, p["W"], p["E"], False))
        # determine the alignment
        maxOpt = 0
        for i in xrange(0, len(o)):
            if len(o[i]) == 2:
                o[i] = [o[i][0], "", o[i][1]]
            elif len(o[i]) == 1:
                o[i] = [o[i][0], "", ""]
            if len(o[i]) != 3:
                raise Exception("Invalid option-string length: " + len(o[i]))
            if o[i][0][0] != "-":
                o[i][0] = "-" + o[i][0]
            if o[i][1] != "":
                o[i][1] = " " + o[i][1]
            maxOpt = max(maxOpt, len(o[i][0]) + len(o[i][1]))
        maxOpt = max(maxOpt, w//5 - len(p["W"] + p["E"]) - 2)
        # print tha ligned options
        wrapper = textwrap.TextWrapper()
        wrapper.width = w - len(p["W"] + p["E"]) - 6 - maxOpt
        for opt in sorted(o):
            printed = False
            for line in wrapper.wrap(opt[2]):
                ostr = opt[0] + opt[1]
                ostr = "   " + ostr + " "*(maxOpt - len(ostr)) + "  "
                if printed:
                    ostr = " "*len(ostr)
                ret.append(toWidthString(ostr + line, w, p["W"], p["E"], False))
                printed = True

    if p["SW"]:
        ret.append(p["SW"] + (w-len(p["SW"] + p["SE"]))*p["S"] + p["SE"])
    return "\n".join(ret)

def prettybox(cmd_args):
    author = getpass.getuser()
    date_arg = datetime.date.today().strftime("%Y-%b-%d")
    box_options = []
    big_box = False
    title = ""
    width = 78
    prefabs = {}
    prefabs["box"]=    [u"-",      u"+",      u"|",      u"+",      u"-",      u"+",      u"|",      u"+"]
    prefabs["block"]=  [u"",       u"",       u"",       u"",       u"",       u" */",    u" *",     u"/*"]
    prefabs["doc"]=    [u"*",      u"* ",     u"* ",     u"/",      u"*",      u" *",     u" *",     u"/*"]
    prefabs["inline"]= [u"-",      u"+",      u"|",      u"+",      u"-",      u"//",     u"//",     u"//"]
    prefabs["plain"]=  [u"",       u"",       u"",       u"",       u"",       u"",       u"",       u""]
    prefabs["shell"]=  [u"=",      u"#",      u"#",      u"#",      u"=",      u"#",      u"#",      u"#"]
    prefabs["tex"]=    [u"=",      u"%",      u"%",      u"%",      u"=",      u"%",      u"%",      u"%"]
    prefabs["ucurve"]= [u"\u2500", u"\u256E", u"\u2502", u"\u256F", u"\u2500", u"\u2570", u"\u2502", u"\u256D"]
    prefabs["udouble"]=[u"\u2550", u"\u2557", u"\u2551", u"\u255D", u"\u2550", u"\u255A", u"\u2551", u"\u2554"]
    prefabs["uthick"]= [u"\u2501", u"\u2513", u"\u2503", u"\u251B", u"\u2501", u"\u2517", u"\u2503", u"\u250F"]
    prefabs["vim"]=    [u"=",      u"\"",     u"\"",     u"\"",     u"=",      u"\"",     u"\"",     u"\""]
    directions=        ["N",       "NE",      "E",       "SE",      "S",       "SW",      "W",       "NW"]
    aliases = {
            "c":"doc",
            "cmake":"shell",
            "cpp":"doc",
            "dl":"inline", # souffle datalog files use C++ comments
            "groovy":"doc",
            "h":"doc",
            "hpp":"doc",
            "java":"doc",
            "python":"shell",
            "sh":"shell",
            }
    pieces={directions[i] : prefabs["box"][i] for i in xrange(0, len(directions))}
    try:
        opts, args = getopt.getopt(cmd_args, "a:d:o:t:w:bh", [d + "=" for d in directions] + ["help"] + prefabs.keys() + aliases.keys())
    except getopt.error, msg:
        print msg
        print "for help use --help"
        sys.exit(2)
    for o, a in opts:
        if o == "-a":
            author = a
        elif o == "-b":
            big_box = True
        elif o == "-d":
            date_arg = a
        elif o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif o == "-o":
            box_options += [a.split(":")]
        elif o == "-t":
            title = a
        elif o == "-w":
            width = int(a)
        elif o[2:] in prefabs.keys():
            pieces={directions[i] : prefabs[o[2:]][i] for i in xrange(0, len(directions))}
        elif o[2:] in aliases.keys():
            pieces={directions[i] : prefabs[aliases[o[2:]]][i] for i in xrange(0, len(directions))}
        else:
            pieces[o[2:]] = a # the cardinal directions
    message = " ".join(args)
    if big_box or (title != ""):
        return boxerize(pieces, message, w=width, t=title, a=author, d=date_arg, o=box_options)
    else:
        return boxerize(pieces, message)

if __name__ == "__main__":
    print prettybox(sys.argv[1:])
