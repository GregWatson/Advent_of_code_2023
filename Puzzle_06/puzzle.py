#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )
#seeds_patt = re.compile("seeds: (.*)")
#map_name_patt = re.compile("([a-z-]+) map:.*")
#range_patt = re.compile(r"(\d+)\s*(\d+)\s*(\d+)")


def load_db():
    db = []
    #get file object
    f = open(input_file_name, "r")

    while(True):
        line = f.readline()
        #if line is empty, you are done with all lines in the file
        if not line:
            break
        #you can access the line
        db.append(line.strip())

    f.close
    return db


#---------------------------------------------------------------------------------------
# Load input

time = [58,    99,   64,   69]
dist = [478, 2232, 1019, 1071]

total = 1
for (i,t) in enumerate(time):
    sum = 0
    d = dist[i]
    for hold_time in range(t):
        d_travelled = (t-hold_time)*hold_time
        if d_travelled > d:
            sum = sum + 1
    total = total * sum
print(f"{total}")


t = 58996469
d = 478223210191071 
sum = 0
for hold_time in range(t):
    d_travelled = (t-hold_time)*hold_time
    if d_travelled > d:
        sum = sum + 1
print(f"{sum}")