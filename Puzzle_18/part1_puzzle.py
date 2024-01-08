#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
dirs='LRUD'
L=0
R=1
U=2
D=3
grid = None
x_max = 0
y_max= 0
print_on = False
colmap = { 0 : '#000'}

class Instr:
    def __init__(self,dir,distance,col, int_col):
        self.dir = dir
        self.distance = distance
        self.col = col  # color string in hex
        self.int_col = int_col

    def print(self):
        print(f"{self.dir} {self.distance} {self.col} {self.int_col}")

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_instructions(db):
    global colmap
    I = []
    for l in db:
        m = re.match(r'(L|U|R|D) (\d+) \(\#([0-9a-f]+)\)', l)
        if m:
            instr = Instr( dirs.find(m.group(1)), int(m.group(2)), m.group(3), int(m.group(3),16 ) )
            # instr.print()
            I.append(instr)
            colmap[instr.int_col] = instr.col
    return I, colmap

def get_dimensions(instrs):
    x_max = 0
    x_min = 0
    y_max = 0
    y_min = 0
    x = 0
    y = 0
    for ins in instrs:
        if ins.dir == L: x=x-ins.distance
        elif ins.dir == R: x=x+ins.distance
        elif ins.dir == U: y=y-ins.distance
        elif ins.dir == D: y=y+ins.distance
        else:
            sys.exit(1)
        if x > x_max: x_max = x
        if x < x_min: x_min = x
        if y > y_max: y_max = y
        if y < y_min: y_min = y
    return(x_max - x_min +1, y_max - y_min +1, 0-x_min, 0-y_min)

def apply_instrs(grid, instrs, x_start, y_start):
    x = x_start
    y = y_start
    edge = 0
    for ins in instrs:
        for step in range(ins.distance):
            if ins.dir == L: x=x-1
            elif ins.dir == R: x=x+1
            elif ins.dir == U: y=y-1
            elif ins.dir == D: y=y+1
            else:
                sys.exit(1)
            grid[y][x]=ins.int_col
            edge = edge + 1
    return edge

def print_grid(grid):
    for row in grid:
        for col in row:
            if col == 0:
                print(f" ", end='')
            else:
                print(f"#", end='')
        print('')

def gen_svg(filename, grid, x_width, y_width, scale=4):
    global colmap
    svg = f"<svg version=\"1.1\" width=\"{x_width*scale}\" height=\"{y_width*scale}\" xmlns=\"http://www.w3.org/2000/svg\">\n"
    # svg = svg + r'   <rect x="25" y="25" width="200" height="200" fill="lime" stroke-width="4" stroke="red" />' + "\n"
    text_file = open(filename, "w")
    text_file.write(svg)
    for y,row in enumerate(grid):
        for x,col in enumerate(row):
            svg = f'   <rect x=\"{scale*x}\" y=\"{scale*y}\" width=\"{scale}\" height=\"{scale}\" '
            svg = svg + f'fill=\"#{colmap[col]}\"  stroke=\"#{colmap[col]}\"/>' + "\n"
            text_file.write(svg)
    svg = svg + r'</svg>' + "\n"
    text_file.write(svg)
    text_file.close()

def add_cube(grid,L, x,y):
    if x<0 or x>=len(grid[0]): return 
    if y<0 or y>=len(grid): return 
    if grid[y][x] != 0: return 
    L.append((x,y))

def fill_grid(grid):
    # find start
    y = 20
    x = 0
    c = 0
    while grid[y][x]==0: x=x + 1
    x=x+1
    print(f"Starting fill at {x},{y}")
    assert grid[y][x] == 0
    L = [ (x,y) ]
    while len(L):
        x,y = L.pop()
        if c % 10000 == 0: print(f"{c} {x},{y}\r",end='')
        if grid[y][x] == 0:
            c = c+1
            grid[y][x]=1
            add_cube(grid,L,x+1,y)
            add_cube(grid,L,x-1,y)
            add_cube(grid,L,x,y+1)
            add_cube(grid,L,x,y-1)
    return c


#---------------------------------------------------------------------------------------
# Load input
db = load_db()

instrs, colmap = get_instructions(db)

(x_width, y_width, x_start, y_start) = get_dimensions(instrs)
print(f"X_width:{x_width} Y_width:{y_width}   start:{x_start},{y_start}")

grid=[ array.array('L', [0] * x_width) for y in range(len(instrs)) ]

edge_len = apply_instrs(grid, instrs, x_start, y_start)

fill_count = fill_grid(grid)
print(f"edge: {edge_len}  fill:{fill_count}    total:{edge_len+fill_count}")
#print_grid(grid)
#gen_svg('out.svg', grid, x_width, y_width, scale=4)