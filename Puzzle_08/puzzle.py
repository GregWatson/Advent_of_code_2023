#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )
#seeds_patt = re.compile("seeds: (.*)")
#map_name_patt = re.compile("([a-z-]+) map:.*")
#range_patt = re.compile(r"(\d+)\s*(\d+)\s*(\d+)")
types = [ 'high_card', 'one_pair', 'two_pair', 'three', 'full_house', 'four', 'five']
dirL = [*'LRLRRLLRRLRRRLRLRRRLLRRLLLLRRRLRRRLRRLRRLRRRLRRRLLRRLRLRRLRRRLLLRRLRRLLRLLRRRLRRRLLRLRRRLRLLRRLLLRLRRRLRRRLRRRLLRLRRRLLRRLRLRLLRRLRRRLRRLRLLRLRRRLRRLRLRLRRLRRRLRRRLRRRLRRLRRRLLRRLRRLLRRRLLRLRLRLRLLLRRLRLRRLRRLRRLRRLRRRLRRRLRLRRRLRLRRRLRRLRLLRLRRLRLRLLLRLLLRRRLRRLLLRLRRRR']

def get_turn():
    index = 0
    while index < len(dirL):
        yield dirL[index]
        index = index + 1
        if index >= len(dirL): index = 0

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

# Done if all positions end in 'Z'
def not_done(c_pos):
    for pos in c_pos:
        if pos[2] != 'Z': return True # i.e. not done
    return False

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

map = {}
# PNM = (QGP, BFT)
for l in db:
    m = re.match(r"([A-Z]+) = \(([A-Z]+), ([A-Z]+)\)",l )
    if m:
        s=m.group(1)
        l=m.group(2)
        r=m.group(3)
        print(f"{s}->{l,r}")
        map[s] = (l,r)

t = get_turn()
num_turns = 0 
pos = 'AAA'
while pos != 'ZZZ':
    turn = next(t)
    pos = map[pos][0] if turn == 'L' else map[pos][1]
    num_turns = num_turns + 1

print(f"{num_turns}")

# get starts - any loc that end in 'A'
c_pos = [ p for p in map if p[2]=='A']  # list of current positions
#print(f"{c_pos}")
t = get_turn()
num_turns = 0
while not_done(c_pos):
    turn = next(t)
    num_turns = num_turns + 1
    if num_turns & 0xfffff == 0 : print(f"{num_turns}\r")
    for i,p in enumerate(c_pos):
        c_pos[i] = map[p][0] if turn == 'L' else map[p][1]

print(f"{num_turns}")