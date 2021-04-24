#!/usr/bin/env python3
"""
+-------------------------------------------------------------------------+
|                              quernspin.py                               |
|                                                                         |
| Author: nic                                                             |
| Date: 2020-Jul-05                                                       |
|                                                                         |
| Options:                                                                |
|   -h           Display this help message                                |
+-------------------------------------------------------------------------+
"""

__doc__ = __doc__.strip()

Q=[
        "7r--7ir7l-",
        "7ljr-jl-jl",
        "r-jil7r--7",
        "---jYiir7l",
        "l--jl-jl-7",
        ]

UP=0
LEFT=1
DOWN=2
RIGHT=3
END=-1

def ortho(hdr):
    return (hdr+2)%4

def sym_to_edge(sym):
    return {
        "-":[LEFT, RIGHT],
        "i": [UP, DOWN],
        "l": [UP, RIGHT],
        "r": [RIGHT, DOWN],
        "7": [DOWN, LEFT],
        "j": [LEFT, UP],
        "Y": [DOWN, END],
    }[sym]

def next_hdr(row, col, hdr):
    edg = sym_to_edge(Q[row][col])
    orth = ortho(hdr)
    if edg[0] == orth:
        return edg[1]
    elif edg[1] == orth:
        return edg[0]
    return None

def solveperm(perm):
    row = 0
    col = perm[0]
    hdr = DOWN
    while True:
        nxt_hdr = next_hdr(row, col, hdr)
        if nxt_hdr is None:
            return False
        elif nxt_hdr == END:
            return True

    return True

def solve():
    for i in range(0, 100000):
        si = str(i)
        si = "000000"+si
        si = si[-5:]
        perm = [int(s) for s in str(si)]
        if solveperm(perm):
            print(perm)
            return


solve()
