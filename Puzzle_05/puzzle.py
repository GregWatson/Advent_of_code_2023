#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )
seeds_patt = re.compile("seeds: (.*)")
map_name_patt = re.compile("([a-z-]+) map:.*")
range_patt = re.compile(r"(\d+)\s*(\d+)\s*(\d+)")

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

def parse_file(db):
    seeds = None
    maps = {}
    map_list = []
    cur_map_name = None
    for l in db:
        m = seeds_patt.match(l)
        if m:
            seeds_l = m.group(1).split()
            seeds = [int(i) for i in seeds_l]
            #  print(f"Saw seeds {seeds}")
            continue
        m = map_name_patt.match(l)
        if m:
            cur_map_name = m.group(1)
            print(f"Creating map file {cur_map_name}")
            maps[cur_map_name] = [] # list of 3-tuples
            map_list.append(cur_map_name)
            continue
        m = range_patt.match(l)
        if m:
            if cur_map_name != None:
                dst_r = int(m.group(1))
                src_r = int(m.group(2))
                len_r = int(m.group(3))
                maps[cur_map_name].append((dst_r, src_r, len_r))
                #print(f"Saw range {dst_r} {src_r} {len_r}")

                continue
            else:
                #print(f"Error: saw range but dont have map name")
                sys.exit(1)

        #Other
        cur_map_name = None
    return seeds, maps, map_list

def get_dst(id, c_map):
    dst = id
    for (dst_r, src_r, len_r) in c_map:
        if (id >= src_r) and (id < src_r+len_r): # in range
            dst = dst_r + (id - src_r)
            return dst
    return dst


def get_location(seed, maps, map_list):
    id = seed
    for map_name in map_list:
        c_map = maps[map_name]
        dst = get_dst(id, c_map)
        # print(f"    Seed {seed}: {id} -> {dst}")
        id = dst
    # print(f"Seed {seed} has loc {id}")
    return dst

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")
(seeds, maps, map_list) = parse_file(db)

for map_name in map_list:
    c_map = maps[map_name]
    # print(f"Map {map_name} has tuples: {c_map}")
dst = 1674914158
for seed in seeds:
    loc = get_location(seed, maps, map_list)
    if loc < dst:
        dst = loc
print(f"{dst} \n\n--------------------\nPart 2")

dst = 1674914158
seed_pairs = []
for x in range(len(seeds) >> 1):
    seed_pairs.append((seeds[2*x], seeds[2*x+1]))
print(f"Seed pais {seed_pairs}")
for (st, le) in seed_pairs:
    print(f"Working on pair {st},{le}")
    seed = st
    for i in range(le):
        loc = get_location(seed, maps, map_list)
        if loc < dst:
            dst = loc
            print(f"New lowest is {dst}")
        seed = seed+1

print(f"{dst} ")



