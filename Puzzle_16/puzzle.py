#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_dir(dir, c):
    if dir[0]==1 and dir[1]==0: # right
        if c =='/': return (0,-1)
        if c =='\\': return (0,1)
    if dir[0]==-1 and dir[1]==0: # left
        if c =='/': return (0,1)
        if c =='\\': return (0,-1)
    if dir[0]==0 and dir[1]==1: # down
        if c =='/': return (-1,0)
        if c =='\\': return (1,0)
    if dir[0]==0 and dir[1]==-1: # up
        if c =='/': return (1,0)
        if c =='\\': return (-1,0)
    print(f"Error {dir}  {c}")
    sys.exit(1)

def get_newxy(x,y,dir):
    newx= x+dir[0]
    newy= y+dir[1]
    return (newx, newy)

def trace_ray(db, used_splitters, energized, x_max, y_max, x=0, y=0, dir=(1,0), count=0):
    # print(f"Starting trace count is {count}")
    while (x >= 0 and x < x_max) and (y >= 0 and y < y_max):
        energized[y][x] = 1
        c = db[y][x]
        if (c == '.' or (c =='|' and dir[0]==0) or (c=='-' and dir[1]==0)) :
            x,y = get_newxy(x,y,dir)
        elif c == '/' or c == '\\':
            dir = get_dir(dir,c)
            x,y = get_newxy(x,y,dir)
        elif c == '-': # split right and left. dir is up or down
            if used_splitters[y][x]: return  # already did this splitter.
            used_splitters[y][x] = 1
            # Process left splitter
            trace_ray(db, used_splitters, energized, x_max, y_max, x-1, y, (-1,0), count = count+1)
            # process right splitter
            dir = (1,0)
            x,y = get_newxy(x,y,dir)
        elif c == '|': # split up and down. dir is left or right
            if used_splitters[y][x]: return  # already did this splitter.
            used_splitters[y][x] = 1
            # Process up splitter
            trace_ray(db, used_splitters, energized, x_max, y_max, x, y-1, (0,-1), count = count+1)
            # process down splitter
            dir = (0,1)
            x,y = get_newxy(x,y,dir)

def zero_arrays(a,b):
    for y in range(len(a)):
        for x in range(len(a[0])):
            a[y][x] = 0
            b[y][x] = 0

def check_sum(energized, x,y, max_energized):
    tot = 0
    for l in energized: tot += sum(l)
    return tot if tot > max_energized else max_energized

#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#print(f"{db}")
x_max = len(db[0])
y_max = len(db)
print(f"Read {y_max} words from {input_file_name}. First Line length is {x_max}.")

used_splitters = [ array.array('i', [ 0 for j in range(x_max) ] ) for i in range(y_max) ]
energized = [ array.array('i', [ 0 for j in range(x_max) ] ) for i in range(y_max) ]
# print(f"{used_splitters}")

trace_ray(db, used_splitters, energized, x_max, y_max)

tot = 0
for l in energized: tot += sum(l)

print(f"Part 1: tot = {tot}")

max_energized = 0
for y in range(y_max):
    #print(f"type of energized is {type(energized)}")
    zero_arrays(energized, used_splitters)
    x=0
    trace_ray(db, used_splitters, energized, x_max, y_max,x=x,y=y,dir=(1,0))
    max_energized = check_sum(energized, x,y, max_energized)

    zero_arrays(energized, used_splitters)
    x=x_max-1
    trace_ray(db, used_splitters, energized, x_max, y_max,x=x,y=y,dir=(-1,0))
    max_energized = check_sum(energized, x,y, max_energized)

for x in range(x_max):
   
    zero_arrays(energized, used_splitters)
    trace_ray(db, used_splitters, energized, x_max, y_max,x=x,y=0,dir=(0,1))
    max_energized = check_sum(energized, x,y, max_energized)
    
    zero_arrays(energized, used_splitters)
    trace_ray(db, used_splitters, energized, x_max, y_max,x=x,y=y_max-1,dir=(0,-1))
    max_energized = check_sum(energized, x,y, max_energized)

print(f"Part 2: tot = {max_energized}")
