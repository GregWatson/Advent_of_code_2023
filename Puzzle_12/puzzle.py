#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )


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

def get_reports(db):
    reps = []
    for l in db:
        data = l.split()
        s = '?'.join([data[0],data[0],data[0],data[0],data[0]])
        n = ','.join([data[1],data[1],data[1],data[1],data[1]])
        nums=n.split(',')
        num=0
        for n in nums:
            num=100*num + int(n)
        # print(f"{data[1]} {num}")
        reps.append((s, num))
    return reps

# Return sequence ID for s. String is only . or #
def get_sequence_from_good_string(s):
    seq  = 0
    count = 0
    for c in s:
        if c == '#': count = count+1
        else:
            if count != 0: seq = seq * 100 + count
            count = 0
    if count != 0: seq = seq * 100 + count
    return seq

# return list of all poss seqs.
def get_all_seqs(s):
    #print(f"get_all_seqs for {s}")
    # find first ?
    p = s.find('?')
    #print(f"  s is now {s} len={len(s)} pos is {p}")
    if p == -1:
        ret = [s]
        # print(f"  returns {ret}")
        return ret  # no ? in string
    length = len(s)
    if length == 1: 
        ret = ['.', '#']
        # print(f"  returns {ret}")
        return ret  # no ? in string
    if p == 0:
        l_str = ''
        r_str = s[1:]
    elif p == length-1: # ? was the last char
        l_str = s[0:p]
        r_str = ''
    else: # ? was not first and not last
        l_str = s[0:p]
        r_str = s[p+1:]
    r_seq = get_all_seqs(r_str)
    #print(f"  l_str is {l_str}  r_str is {r_str}   r_seq is {r_seq}")
    good_seqs = [ l_str + '.' + str for str in r_seq]
    bad_seqs = [ l_str + '#' + str for str in r_seq]
    #print(f"s is {s}  r_seq is {r_seq}  good {good_seqs}   bad {bad_seqs}")
    good_seqs.extend(bad_seqs)
    #print(f"  returns {good_seqs}")
    return good_seqs

def get_combs(r):
    # print(f"get valid combs for {r}")
    s = r[0]   # string
    s_ID = r[1]
    all_seqs = get_all_seqs(s)
    # print(f"seqs for {s} are\n{all_seqs}")
    valids = []
    for seq in all_seqs:
        if get_sequence_from_good_string(seq) == s_ID:
            valids.append(seq)

    return valids

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

reps = get_reports(db) # list of tuple ( orig_string, seq_ID)
#s = '.##.#...#..........##.....#........#......#....'
#print(f"{s} -> {get_sequence_from_good_string(s)}")


tot = 0
for r in reps:
    # r = ('?.???????..?##???', 603)
    print(f"Process{r}")
    combs = get_combs(r)
    print(f"Valids for {r} are {combs}")
    tot = tot + len(combs)
    # break
print(f"tot is {tot}")