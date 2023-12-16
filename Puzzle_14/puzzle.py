#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'

def load_db():
    with open(input_file_name) as f:
        lines = f.read().splitlines()
    return lines


def tilt_platform_north(p):
    for y, l in enumerate(p):
        if y == 0 : next
        for x in range(len(l)):
            c = p[y][x]
            if c=='O':
                new_y = y-1
                while new_y >= 0 and p[new_y][x] == '.': 
                    new_y = new_y - 1
                new_y = new_y+1
                if new_y != y:
                    p[new_y][x] = 'O'
                    p[y][x] = '.'

def tilt_platform_south(p):
    length = len(p)
    len_x = len(p[0])
    for y in range(length-2,-1,-1):
        for x in range(len_x):
            c = p[y][x]
            if c=='O':
                new_y = y+1
                while new_y < length and p[new_y][x] == '.': 
                    new_y = new_y + 1
                new_y = new_y-1
                if new_y != y:
                    p[new_y][x] = 'O'
                    p[y][x] = '.'



def tilt_platform_west(p):
    len_x = len(p[0])
    for y in range(len(p)):
        for x in range(len_x):
            if not x: next
            c = p[y][x]
            if c=='O':
                new_x = x-1
                while new_x >= 0 and p[y][new_x] == '.': 
                    new_x = new_x - 1
                new_x = new_x+1
                if new_x != x:
                    p[y][new_x] = 'O'
                    p[y][x] = '.'

def tilt_platform_east(p):
    len_x = len(p[0])
    for y in range(len(p)):
        for x in range(len_x-2,-1,-1):
            c = p[y][x]
            if c=='O':
                new_x = x+1
                while new_x < len_x and p[y][new_x] == '.': 
                    new_x = new_x + 1
                new_x = new_x-1
                if new_x != x:
                    p[y][new_x] = 'O'
                    p[y][x] = '.'

def print_platform(p):
    for l in p:
        for c in l: print(f"{c}", end='')
        print("")
    print("")

def get_load(p):
    load = 0
    south_edge = len(p)
    for y, l in enumerate(p):
        for x in range(len(l)):
            c = p[y][x]
            if c=='O':
                load = load + (south_edge - y)
    return load

def platforms_are_same(p1, p2):
    for y, l in enumerate(p1):
        for x in range(len(l)):
            if p1[y][x] != p2[y][x]: return False
    return True
#---------------------------------------------------------------------------------------
# Load input
db = load_db()
print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

platform = []
for l in db:
    platform.append( array.array('u',l))

#tilt_platform_north(platform)
#load = get_load(platform)

#print_platform(platform)
# print(f"load {load}")

delta = 0
prev_platform = []
i = 0
while i < 1000000000:
    tilt_platform_north(platform)
    #print_platform(platform)
    tilt_platform_west(platform)
    #print_platform(platform)
    tilt_platform_south(platform)
    #print_platform(platform)
    tilt_platform_east(platform)
    #print_platform(platform)
    print(f"{i}  {delta}")
    if (delta==0) and i>0:
        
        for index, p in enumerate(prev_platform):
            if platforms_are_same(p, platform):
                delta = i - index
                print(f" --- Platforms same {index} and {i}. Delta is {delta} ---")
                while (i+delta < 1000000000) : i=i+delta
                print(f"Jumped to {i}")
                break
    i = i + 1
    prev_platform.append(copy.deepcopy(platform))

print_platform(platform)

load = get_load(platform)
print(f"load {load}")

