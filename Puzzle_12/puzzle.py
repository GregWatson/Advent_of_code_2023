#import argparse
import sys
import re
import functools


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
        s = data[0]
        while '..' in s: # remove multiple dots - they dont do anything useful
            s = s.replace('..','.')
        s = '?'.join([s,s,s,s,s])
        n = ','.join([data[1],data[1],data[1],data[1],data[1]])
        reps.append((s, n))
    return reps

def get_next_num(s): 
    # s is string of numbers 0-99 separated by colons
    # return first number (as int) and new string without that number.
    if not len(s): return (-1, '')
    p = s.find(',')
    if p == -1 : return (int(s),'') # last number
    else: return (int(s[0:p]), s[p+1:])

@functools.cache
def get_valid_strings(s: str, n: int, nums: str ,in_hash=False, lev=0) -> int:
    pad = '   '*lev
    # print(f"{pad}--- str:{s}  n:{n}  nums:{nums}  in:{in_hash}")
    len_s = len(s)
    # print(f"l {len_s}", end="\r")
    len_nums = len(nums)
    if len_s == 0:
        if (n > 0 or len_nums > 0): return 0
        return 1
    c = s[0]
    if n==0 : # at end of current hash sequence - next must be not # or end 
        # If no more brokens to find then we must either be at end of string or no # in the string
        if len_nums == 0:  # just finished the last hash sequence
            if not len_s or not '#' in s: return 1
            else: return 0  # next char in s must be # so fail
        # next char in s must NOT be #
        if c == '#': return 0
        n, nums = get_next_num(nums)
        return get_valid_strings(s[1:], n, nums, in_hash=False, lev=lev+1)
    
    # n > 0. But might not yet have started the current hash
    if c == '.':
        if not in_hash : # Just skip the '.'
            return get_valid_strings(s[1:], n, nums, in_hash=False, lev=lev+1)
        else: # in hash and see '.' - that's a fail
            return 0 # fail

    if c == '#': # ok, start of new hash or continuation
        return get_valid_strings(s[1:], n-1, nums, in_hash=True, lev=lev+1)

    # Next c is ? - need to handle noth cases.
    assert c == '?'

    if in_hash: # '?' can only succeed if treated as '#'
        return get_valid_strings(s[1:], n-1, nums, in_hash=True, lev=lev+1)

    # Not in hash - try both alternatives and sum the results.
    try_hash = get_valid_strings(s[1:], n-1, nums, in_hash=True, lev=lev+1)
    try_dot = get_valid_strings(s[1:], n, nums, in_hash=False, lev=lev+1)
    return try_hash + try_dot

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

reps = get_reports(db) # list of tuple ( orig_string, seq_ID)
#s = '.##.#...#..........##.....#........#......#....'
#print(f"{s} -> {get_sequence_from_good_string(s)}")


tot = 0
for i, r in enumerate(reps):
    # r = ( '.....????..????.?????.????', [1,1,1,1])
    print(f"Line {i} : Working on {r}")
    n, nums = get_next_num(r[1])
    sL = get_valid_strings(r[0], n, nums, in_hash=False, lev=0)
    print(f" -- {sL} valids for {r}")
    if sL: tot = tot + sL
    # break
print(f"tot is {tot}")