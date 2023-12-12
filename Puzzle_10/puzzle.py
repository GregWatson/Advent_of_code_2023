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
nextdir = { # key = (cur_dir, cur char)
    ('N', '|') : 'N',
    ('N', '7') : 'W',
    ('N', 'F') : 'E',
    ('S', '|') : 'S',
    ('S', 'L') : 'E',
    ('S', 'J') : 'W',
    ('W', '-') : 'W',
    ('W', 'L') : 'N',
    ('W', 'F') : 'S',
    ('E', '-') : 'E',
    ('E', 'J') : 'N',
    ('E', '7') : 'S'
}

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

def make_map(db):
    map = []
    for y,l in enumerate(db):
        y_list = []
        for x,c in enumerate(l):
            y_list.append(c)
            if c == 'S':
                start = (x,y)
        map.append(y_list)
    return (start, map)

def find_loop(start, map):
    x=start[0]
    y=start[1]
    dir='E' # specific to this map
    done = False
    steps = 0
    new_map = []
    for i in range(len(map)):
        new_map.append(['.' for x in range (len(map[0]))] )
    while not done:
        # move
        if dir == 'N': y=y-1
        elif dir == 'S': y=y+1
        elif dir == 'W': x = x-1
        else: x=x+1
        c= map[y][x]
        steps = steps + 1
        #print(f"S:{steps} x,y:({x},{y}) char={c}  dir={dir}")
        if c != 'S':
            # find next move if needed
            dir = nextdir[(dir, c)]
        else:
            done = True
        new_map[y][x] = c
    return steps, new_map

def get_count_inside(m):
    for l in m:
        print( ''.join(l))
        state = 'out' # outside loop
        s = ''
        count = 0

        for c in l:
            new_state = state
            if state == 'out':
                if c != '.': 
                    if c in "FL": new_state = 'in_pipe'
                    else : new_state='in'
            elif state == 'in_pipe':
                if c != '-': new_state = 'in'
            elif state == 'out_pipe':
                if c != '-': new_state = 'out'
            else: # inside loop
                if c == '.': count = count + 1
                else:
                    if c != '-': new_state = 'out'
            # new state
            if c == '.' : s = s + ('O' if new_state == 'out' else 'I')
            else: s = s + '+'
            state = new_state
        print(s)

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

(start, map) = make_map(db)

steps, new_map = find_loop(start, map)
print(f"steps:{steps} so half is {steps>>1}")

for l in new_map:
    print( ''.join(l))

c = get_count_inside(new_map)