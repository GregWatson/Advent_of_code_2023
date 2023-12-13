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

def add_space(m):
    m2 = []
    for y in m:
        # double in x dir
        line = []
        for x,c in enumerate(y):
            line.append(c)
            if c in '.|J7': line.append(' ')
            elif c in '-FLS': line.append('-')
            else:
                print(f"Unknown char '{c}'")
                sys.exit(1)
        m2.append(line)
        l = []
        for c in line:
            if c in '.J-LS ': l.append(' ')
            elif c in '|7F': l.append('|')
            else:
                print(f"Unknown char '{c}'")
                sys.exit(1)
        m2.append(l)
    return m2

def add_new_adjacent_locs(x,y,m,stack):
    if m[y][x-1] in ' .': stack.append((x-1,y))
    if m[y][x+1] in ' .': stack.append((x+1,y))
    if m[y-1][x] in ' .': stack.append((x,y-1))
    if m[y+1][x] in ' .': stack.append((x,y+1))


def flood_search(pos, m):
    x,y = (pos[0], pos[1])
    print(f"Start: x{x} y{y}")
    if m[y][x] != '#':
        print(f"Err - bad starting char {m[y][x]}")
        sys.exit(1)
    m[y][x] = ' '
    stack = [(x,y)]  # unchecked locations
    done = False
    count = 0
    while len(stack):
        (x,y) = stack.pop()
        c = m[y][x]
        if c == '.': count = count + 1
        m[y][x] = '#'
        add_new_adjacent_locs(x,y,m,stack)


    return count


#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

(start, map) = make_map(db)

steps, new_map = find_loop(start, map)
print(f"steps:{steps} so half is {steps>>1}")

for l in new_map:
    print( ''.join(l))

# Double each direction to add spaces
map2 = add_space(new_map)

start=(81, 13)

map2[start[1]][start[0]] = '#'

c = flood_search(start, map2)

for l in map2:
    print(''.join(l))

print(f"Count inside loop is {c}")
