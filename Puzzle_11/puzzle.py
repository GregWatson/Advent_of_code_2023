#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )


def load_db():
    db = []
    #get file object
    f = open(input_file_name, "r")
    while(True):
        line = f.readline()
        #if line is empty, you are done with all lines in the file
        if not line:
            break
        db.append(line.strip())
    f.close
    return db

def get_stars(m):
    s = []
    for y in range(len(m)):
        for x in range(len(m[0])):
            if m[y][x] == '#':
                s.append((x,y))
    return s

# return number of numbers in l that have value less than v
def get_num_before(v, l):
    c = 0
    for j in l: 
        if j < v: c = c + 1
        if j >= v:
            break
    return c

def get_dist_tot(star_list):
    ss = star_list[:]
    dist_tot=0
    while len(ss) > 1:
        s1 = ss.pop()
        for s2 in ss:
            dist = abs(s1[0]-s2[0]) + abs(s1[1] - s2[1])
            print(f"Dist ({s1} to {s2} is {dist}.  dist_tot = {dist_tot})")
            dist_tot = dist_tot + dist
    return dist_tot

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

orig_stars = get_stars(db)

#expand in Y
ml = []
empty_rows = []
for i, l in enumerate(db):
    ml.append(l)
    if '#' not in l:
        ml.append(l)
        empty_rows.append(i)
print(f"Expand Y: {len(ml)-len(db)}")

#get list of all columns
empty_cols = []
for x in range(len(db[0])):
    for l in db:
        if l[x] == '#':
            break
    else:
        empty_cols.append(x)
print(f"Expand x: {len(empty_cols)}")

#expand in X
m = []
for l in ml:
    line=''
    for i,c in enumerate(l):
        line=line+c
        if i in empty_cols:
            line=line+'.'
    m.append(line)

# Print expanded universe
for l in m:
    print(l)

star_list = get_stars(m)

for s in star_list:
    print(f"({s[0]},{s[1]})")
print(f"Saw {len(star_list)} stars")

dist_tot = get_dist_tot(star_list)

print(f"Dist tot = {dist_tot}")

#######################
# Part 2

mil_stars = []
for s in orig_stars:
    new_x = get_num_before(s[0], empty_cols) * 999999 + s[0]
    new_y = get_num_before(s[1], empty_rows) * 999999 + s[1]
    mil_stars.append((new_x, new_y))
    print(f"({s[0]},{s[1]} -> ({new_x},{new_y}))")
dist_tot = get_dist_tot(mil_stars)

print(f"Saw {len(mil_stars)} stars")
print(f"cols: {empty_cols} \nrows {empty_rows}")
print(f"Dist tot = {dist_tot}")

