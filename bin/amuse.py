"""
+-------------------------------------------------------------------------+
|                                amuse.py                                 |
|                                                                         |
| Author: Nic H.                                                          |
| Date: 2016-Oct-09                                                       |
|                                                                         |
| Wrapper for the beets library, allowing better musical selection and    |
| automatic launching of VLC to play the music.                           |
|                                                                         |
| usage: amuse [OPTIONS] [FILTER]                                         |
|                                                                         |
| plays the songs in the beet library filtered by [FILTER] using VLC      |
|                                                                         |
| Options:                                                                |
|   -a <rx>    filter artists with the regular expression <rx>            |
|   -g <rx>    filter the file-path with regular expression <rx>          |
|   -h         display this help message                                  |
|   -l         list the available albums                                  |
|   -m <rx>    filter albums with the regular expression <rx>             |
|   -r <num>   choose <num> tracks to play at random(ish)                 |
|   -s         shuffle the songs, playing them out-of-order               |
|   -t <rx>    filter track names with the regular expression <rx>        |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

import getopt
import os
import random
import re
import subprocess
import sys
import unicodedata

class Amused:
    def __init__(self):
        self.beet_args = []
        self.rx_general = ""
        self.rx_artist = ""
        self.rx_album = ""
        self.rx_title = ""
        self.random = -1
        self.shuffle = False
        self.playlist = []

    def regenerate(self):
        # read from the beet process
        proc = subprocess.Popen(["beet", "ls", "-p"] + self.beet_args, stdout=subprocess.PIPE)
        self.playlist = [path_to_tuple(line.strip()) for line in proc.stdout.readlines()]
        if not proc.wait() == 0:
            sys.exit(1)
        # filter using the advanced regexes
        rxp_general = re.compile(self.rx_general, re.I)
        rxp_artist  = re.compile(self.rx_artist,  re.I)
        rxp_album   = re.compile(self.rx_album,   re.I)
        rxp_title   = re.compile(self.rx_title,   re.I)
        self.playlist = [t for t in self.playlist if re.search(rxp_general, "/".join(t[1:]))]
        self.playlist = [t for t in self.playlist if re.search(rxp_artist,  t[1])]
        self.playlist = [t for t in self.playlist if re.search(rxp_album,   t[2])]
        self.playlist = [t for t in self.playlist if re.search(rxp_title,   t[3])]
        # shuffle, random, or ordered
        # TODO random
        if self.shuffle:
            random.shuffle(self.playlist)
        else:
            self.playlist.sort(key=lambda t: (t[2]+t[3]).lower())

    def play(self):
        paths = [os.path.join(*t) for t in self.playlist]
        subprocess.Popen(["vlc", "--one-instance"] + paths, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def path_to_tuple(p):
    (tmp, title) = os.path.split(p.decode("utf-8")) # hard coding because i am the only person who actually uses
    (tmp2, album) = os.path.split(tmp)
    (rest, artist) = os.path.split(tmp2)
    return (rest, artist, album, title)

_strong_width_map={}
def strong_width(s):
    if not s in _strong_width_map:
        w = 0
        for c in s:
            w += 2 if unicodedata.east_asian_width(c) in ("F", "W") else len(unicodedata.normalize('NFC', c))
        _strong_width_map[s] = w
    return _strong_width_map[s]

def strong_format(s, w):
    return s + " "*(w-strong_width(s))

def display_confirm(instance):
    instance.regenerate()
    ret = False
    while(not ret):
        # show the current selection
        artist, album, title = 0, 0, 0;
        for n in instance.playlist:
            artist = max(artist, strong_width(n[1]))
            album  = max(album,  strong_width(n[2]))
            title  = max(title,  strong_width(n[3]))
        for n in instance.playlist:
            print(strong_format(n[1], artist), " | ", strong_format(n[2], album), " | ", strong_format(n[3], title))
        # confirm playlist with the user
        redo = not instance.random == -1 or instance.shuffle
        s = input("Play? [Y/n" + ("/r" if redo else "") + "] ")
        if "n" in s or "N" in s:
            break
        elif redo and ("r" in s or "R" in s):
            instance.regenerate()
        else:
            ret = True
    return ret

def amuse():
    instance = Amused()
    try:
        opts, args = getopt.getopt(sys.argv[1:], "a:g:m:hlr:st:", ["help"])
    except getopt.error as err:
        print(err.msg)
        print("for help use --help")
        sys.exit(2)
    for o, a in opts:
        # flags
        if o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif o == "-l":
            subprocess.check_call(["beet", "ls", "-a"])
            sys.exit(0)
        elif o == "-s":
            instance.shuffle = True
        # arguments
        elif o == "-a":
            instance.rx_artist = a;
        elif o == "-g":
            instance.rx_general = a;
        elif o == "-m":
            instance.rx_album = a;
        elif o == "-r":
            instance.random = int(a)
        elif o == "-t":
            instance.rx_title = a;
    instance.beet_args = args
    if (display_confirm(instance)):
        instance.play()

if __name__ == "__main__":
    amuse()
