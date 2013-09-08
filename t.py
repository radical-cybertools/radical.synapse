#!/usr/bin/python 

import os

I = int(os.environ['ITER'])
L = 10 ** 5
f = 3.1415926


for   i in range (0, I) :
  for j in range (0, L) :
    f = 0.50 * f
    f = 2.00 * f
    f = 0.50 * f
    f = 0.50 * f
    f = 4.00 * f
    f = 0.50 * f
    f = 2.00 * f
    f = 0.50 * f
    f = 0.50 * f
    f = 4.00 * f



