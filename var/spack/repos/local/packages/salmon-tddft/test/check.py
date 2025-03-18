import os
import sys

with open('outfile','r') as f:
    for line in f:
       line = f.readline()
       if 'end SALMON' in line:
          print(line)

f.close()
