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

def get_cmds():
    with open(input_file_name) as f:
        s = ''
        while(1):
            char = f.read(1)          
            if not char: 
                break
            else: 
                    if ord(char) >= 32 : s = s + char
        return s


def get_HASH(s):
    h = 0
    for c in s:
        h = (17 * (h + ord(c))) % 256
    return h

# each box is a list of lenses

def remove_lens(label, boxes):
    print(f"Remove lens {label}")
    box = boxes[get_HASH(label)]
    for i,l in enumerate(box):
        print(f"lens is {l}")
        if l[0] == label:
            del box[i]


def add_lens(cmd_lens, boxes):
    label,focus = cmd_lens
    print(f"Add lens {label} focus {focus}")
    box = boxes[get_HASH(label)]
    for i,l in enumerate(box):
        if l[0] == label: # replace
            box[i] = cmd_lens
            break
    else:
        box.append(cmd_lens)

def part2(db):
    boxes = [ [] for i in range(256)]
    for s in db:
        print(f"{s}")
        m = re.match(r'([a-z]+)-',s)
        if m: 
            remove_lens(m.group(1), boxes)
        else:
            m = re.match(r'([a-z]+)=(\d)',s)
            if m: 
                add_lens((m.group(1), int(m.group(2))), boxes)


    tot = 0
    for bi, box in enumerate(boxes):
        for li,l in enumerate(box):
            v = (bi+1) * (li + 1) * l[1]
            tot += v
    return tot

#---------------------------------------------------------------------------------------
# Load input
s = get_cmds()
db = s.split(',')
print(f"Read {len(db)} words from {input_file_name}. First Line length is {len(db[0])}.  Chars read {len(s)}")

tot = 0
label2box  = {}
for i,s in enumerate(db):
    label2box[s] = get_HASH(s)
    tot = tot + label2box[s]

print(f"tot {tot}")

tot = part2(db)
print(f"tot {tot}")
