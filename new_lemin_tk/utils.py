#!/usr/bin/env python3

import sys
import random
import string 

def eprint(err):
    print(err, file=sys.stderr) 

def parser_eprint(err, l):
    eprint("error: line " + str(l) + ": " + err)

def get_int(s):
    try:
        i = int(s)
        return i
    except ValueError:
        return None

def randstr(size):
    return ''.join(random.choice(string.ascii_uppercase\
            + string.ascii_lowercase + string.digits)\
            for _ in range(size))
