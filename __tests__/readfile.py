#!/usr/bin/env python3

import sys

if len(sys.argv) < 2:
    print("error: no argument")
    exit()

f = open(sys.argv[1])
for line in f:
    print(line, end='')
