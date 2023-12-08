#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )
pattern_number = re.compile("(\d+)")

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

def is_part(y, start_pos, end_pos, db, number, stars):
    # decide if the number at line y, start_pos:end_pos-1 is a part.
    x_min  = 0 if start_pos == 0 else start_pos-1
    x_max = end_pos-1 if end_pos == len(db[0]) else end_pos
    print(f"{y} {x_min}-{x_max}")
    res = False
    if y > 0: # check line above
        for x in range(x_min, x_max+1):
            if db[y-1][x] in syms: 
                if db[y-1][x] == '*': stars[y-1][x].append(number)
            res = True
    if y < len(db)-1:
        for x in range(x_min, x_max+1):
            print(f"{y}:{x} ")
            if db[y+1][x] in syms:
                if db[y+1][x] == '*': stars[y+1][x].append(number)
            res = True
    if start_pos != 0:
        if db[y][start_pos-1] in syms: 
            if db[y][start_pos-1] == '*': stars[y][start_pos-1].append(number)
            res = True
    if end_pos != len(db[0]):
        if db[y][end_pos] in syms: 
            if db[y][end_pos] == '*': stars[y][end_pos].append(number)
            res = True
    return res

def process_line(y, l, db, stars):
    pos = 0
    sum  = 0
    while pos < len(l):
        m = pattern_number.search(l, pos)
        if m:
            number = int(m.group(1))
            start_pos = m.start(1)
            end_pos = m.end(1)
            num_len = end_pos - start_pos
            # print(f"num {number} seen at pos {start_pos} with length {num_len}")
            pos = end_pos

            if is_part(y, start_pos, end_pos, db, number, stars):
                # print(f"{number} is a part")
                sum = sum + number
        else:
            break
    return sum


#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")
sum=0

stars = []
for l in range(len(db)): stars.append([ [] for x in range(len(db[0]))] )

for index, l in enumerate(db):
    sum = sum + process_line(index, l, db, stars)

print("Sum is ", sum)

sum = 0
for l in range(len(db)):
    for x in range(len(db[0])):
        if len(stars[l][x]) == 2:
            num = stars[l][x][0] * stars[l][x][1]
            sum = sum + num

print("Sum is ", sum)
