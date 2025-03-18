import os
import sys

flg = 0
with open('LOG.pe000000','r') as f:
    for line in f:
       if '      [V]' in line:
          flg = 1
       else:
          flg = 0
       if flg == 1:
          line = f.readline()
          if 'NaN' in line:
             print(" ### Failed")
             print(" ### Found \"NaN\" in the calculation results.")
             sys.exit(-1)
          else:
             val = float(line[13:30])
             if val < -80 or val > 120 :
                print(" ### Failed")
                print(" ### The calculation results are outside the expected range.")
                sys.exit(-1)
          line = f.readline()
          if 'NaN' in line:
             print(" ### Failed")
             print(" ### Found \"NaN\" in the calculation results.")
             sys.exit(-1)
          else:
             val = float(line[13:30])
             if val < -80 or val > 120 :
                print(" ### Failed")
                print(" ### The calculation results are outside the expected range.")
                sys.exit(-1)
       flg = 0
       line = f.readline()

f.close()
print("SCALE test Passed")
