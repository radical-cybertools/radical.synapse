#!/usr/bin/env python

import sys

fname = sys.argv[1]
f     = open (fname, 'r')

for line in f.readlines () :
    line  = line.replace (',', '.')
    elems = line.split   (';')

    if elems[2] == '-------' :
        print '%-10s %10s %7s %7.2f %7.2f %7.2f %5d %5d %5d %5d' \
            % (  str(elems[0]),   str(elems[1]), 
                 str(elems[2]), float(elems[3]), float(elems[4]), float(elems[5]), 
                 int(elems[6]),   int(elems[7]),   int(elems[8]),   int(elems[9]))
    else :
        print '%-10s %10s %7.2f %s %s %s %5d %5d %5d %5d' \
            % (  str(elems[0]),   str(elems[1]), 
               float(elems[2]),   str(elems[3]),   str(elems[4]),   str(elems[5]), 
                 int(elems[6]),   int(elems[7]),   int(elems[8]),   int(elems[9]))

