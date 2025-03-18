import os
import sys

flg = 0
with open('md.log','r') as f:
    for line in f:
       if 'Finished mdrun' in line:
          flg = 1

f.close()

if flg == 1:
  print("GROMACS test Passed")
else:
  print("Error")

