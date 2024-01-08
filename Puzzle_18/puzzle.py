#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
dirs='RDLU'
L=2
R=0
U=3
D=1
grid = None
x_max = 0
y_max= 0
print_on = False
# edges are hash of int (y or x) to list of tuples: (x1,x2) or (y1,y2)
v_edges = {}  # x -> (y1,y2) where y2 > y1
h_edges = {}  # y -> (x1,x2) where x2 > x1
v_edges_x = []
h_edges_y = []
IS_VY1 = 0
IS_VY2 = 1

class Instr:
    def __init__(self,dir,distance):
        self.dir = dir
        self.distance = distance

    def print(self):
        print(f"{self.dir} {self.distance} ")

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_instructions(db):
    I = []
    for l in db:
        m = re.match(r'(L|U|R|D) \d+ \(\#([0-9a-f]{6})\)', l)
        if m:
            hexnum = int(m.group(2),16)
            dir = hexnum & 3
            dist = hexnum >> 4
            instr = Instr( dir, dist)
            # instr.print()
            I.append(instr)
    return I

def get_dimensions(instrs):
    x_max = 0
    x_min = 0
    y_max = 0
    y_min = 0
    x = 0
    y = 0
    last_dir = None
    for ins in instrs:
        if ins.dir == L: x=x-ins.distance
        elif ins.dir == R: x=x+ins.distance
        elif ins.dir == U: y=y-ins.distance
        elif ins.dir == D: y=y+ins.distance
        else:
            print(f"Bad dir")
            sys.exit(1)
        if x > x_max: x_max = x
        if x < x_min: x_min = x
        if y > y_max: y_max = y
        if y < y_min: y_min = y

        if last_dir != None:
            if ((last_dir ^ ins.dir) & 1) != 1:
                print("Expected chnage in dir but saw same dir or reverse")
        last_dir = ins.dir

    return(x_max - x_min +1, y_max - y_min +1, 0-x_min, 0-y_min)

def add_h_line(y,x1,x2):
    global h_edges
    p = (x1, x2) if x1 < x2 else (x2, x1)
    if y in h_edges: 
        h_edges[y].append(p)
        print(f"Appended 2nd hline at y={y}")
    else: h_edges[y] = [p]
    return x2

def add_v_line(x,y1,y2):
    global v_edges
    p = (y1, y2) if y1 < y2 else (y2, y1)
    if x in v_edges: 
        v_edges[x].append(p)
        print(f"Appended 2nd vline at x={x}")
    else: v_edges[x] = [p]
    return y2

def apply_instrs( instrs, x_start, y_start):
    x = x_start
    y = y_start
    edge_len = 0
    v_edges = {}  # x -> (y1,y2) y2 > y1
    h_edges = {}  # y -> (x1,x2) x2 > x1

    for ix,ins in enumerate(instrs):
        if ins.dir == L: 
            x = add_h_line(y,x,x-ins.distance)
        elif ins.dir == R: 
            x = add_h_line(y,x,x+ins.distance)
        elif ins.dir == U: 
            y = add_v_line(x,y,y-ins.distance)
        elif ins.dir == D:
            y = add_v_line(x,y,y+ins.distance)
        else:
            sys.exit(1)
        edge_len = edge_len + ins.distance
        #print(f"I:{ix} Dir:{dirs[ins.dir]} Dist:{ins.distance} Ended at {x},{y}")
    return edge_len

def check_edges(h_edges, v_edges):
    # Every vline end has an associated hline point
    print(f"Checking edges...")
    for x in v_edges:
        for (y1, y2) in v_edges[x]:
            found_y1 = False
            for (x1, x2) in h_edges[y1]:
                if (x1 == x) or (x2 == x): found_y1 = True
            found_y2 = False
            for (x1, x2) in h_edges[y2]:
                if (x1 == x) or (x2 == x): found_y2 = True
            if not found_y1 or not found_y2:
                print(f"vline x:{x} {y1}-{y2}: Found Y1: {found_y1}  Found Y2:{found_y2}")



def get_h_line_area(y):
    global h_edges
    global h_edges_y
    global v_edges
    global v_edges_x
    state = 0 # outside
    x=-1
    c = 0
    last_vy = None
    for vx in v_edges_x:
        for (vy1,vy2) in v_edges[vx]: 
            assert vy2 > vy1
            if y < vy1 or y > vy2: continue
            if y==1176403: print(f"y {y} intersects v-line at x={vx} {vy1}-{vy2}")
            # are we at either end of vline?
            if y==vy1:
                if last_vy == None: # first of horiz pair
                    last_vy = IS_VY1
                    if state == 1: # add length
                        c = c + vx-x-1
                else: # 2nd of horiz pair
                    if last_vy == IS_VY2: # same dir - flip state
                        state = 1 - state
                    last_vy = None
            elif y==vy2:
                if last_vy == None: # first of horiz pair
                    last_vy = IS_VY2
                    if state == 1: # add length
                        c = c + vx-x-1
                else: # 2nd of horiz pair
                    if last_vy == IS_VY1: # same dir - flip state
                        state = 1 - state
                    last_vy = None
            else: # not a line end - just intersecting the middle - flip state
                if last_vy != None:
                    print(f"Err: y:{y} expected last_vy to be None but saw {last_vy}")
                if state == 1: # add length
                    c = c + vx-x-1
                state = 1 - state
            x = vx

    return c

def fill_grid(h_edges, v_edges):
    global h_edges_y
    y = h_edges_y[0]
    y_last = h_edges_y[-1]
    print(f"Start at line {y}. FInish at {y_last}")
    c = 0
    prev_c = 0
    while y < y_last: # No need to do last one
        if y % 100000 == 0 : print(f"{y}  c:{c}         \r",end='')
        #if y in h_edges:
        prev_c = get_h_line_area(y)
        c = c + prev_c
        y = y+1
    return c

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

instrs = get_instructions(db)

(x_width, y_width, x_start, y_start) = get_dimensions(instrs)
print(f"{len(instrs)} instructions. X_width:{x_width} Y_width:{y_width}   start:{x_start},{y_start}")

edge_len = apply_instrs(instrs, x_start, y_start)

print(f"edge len: {edge_len}")

h_edges_y = [ y for y in h_edges]
h_edges_y.sort()
v_edges_x = [ x for x in v_edges]
v_edges_x.sort()

# print(f"\n--- Hlist is: -----")
# for y in h_edges_y:
#     print (f"{y}: ", end='')
#     for ll in h_edges[y]:
#         print(f"{ll}",end='')
#     print("")


check_edges(h_edges, v_edges)

print(f"Saw {len(h_edges)} h_edges and {len(v_edges)} v_edges.")
fill_count = fill_grid(h_edges, v_edges)

print(f"edge: {edge_len}  fill:{fill_count}    total:{edge_len+fill_count}")
#print_grid(grid)
#gen_svg('out.svg', grid, x_width, y_width, scale=0.0001)