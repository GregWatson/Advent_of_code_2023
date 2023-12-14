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
        nums = map(int, n.split(','))
        reps.append((s, list(nums)))
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


def get_valid_strings(s: str,nums: list ,in_hash=False, lev=0) -> list:
    pad = '   '*lev
    # print(f"{pad}--- str:{s}  nums:{nums}  in:{in_hash}")
    len_s = len(s)
    # print(f"l {len_s}", end="\r")
    len_nums = len(nums)
    min_str_len = sum(nums) + len_nums - 1
    if len_s < min_str_len: return 0
    if len_s == 0 and len_nums == 0: return [ '' ]
    if len_s == 0 and len_nums == 1 and nums[0] == 0: return [ '' ]
    if len_s == 0 and len_nums > 0: return [] # fail
    # if no numbers left then there cannot be any hashes left.
    if len_nums == 0:
        if '#' in s: return [] # fail
        # else make sure no ? left
        new_string = s.replace("?", ".")
        return [new_string]  # only possible
    if len_s == 1:
        if (s =='#' and len_nums==1 and nums[0]==1) : 
            # print(f"{pad}Good: return [{s}]") 
            return [s]  # good
        if (s =='?' and len_nums==1 and nums[0]==1) : return ['#']  # good
        if (s =='?' and len_nums==0 ) : return ['.']  # good
        if (s =='.' and len_nums==0 ) : return ['.']  # good
    # string of at least 2 chars, still looking for at least one #
    c = s[0]
    n = nums[0]
    # print(f"{pad}c={c}  n={n}")
    if n==0 and not in_hash:
        print(f"Error. if n is 0 then must be in_hash")
        sys.ext(1)
    if in_hash :
        if n > 0: 
            if c in '#?':
                nums[0] = n-1
                sL = get_valid_strings(s[1:], nums, in_hash, lev=lev+1)
                # print(f"{pad}recursion returned {sL}")
                if len(sL) : 
                    return [ '#' + ss for ss in sL ] 
            return [] # fail
        if n == 0 and c in '.?' : 
            sL = get_valid_strings(s[1:], nums[1:], in_hash=False, lev=lev+1)
            # print(f"{pad}recursion returned {sL}")
            return [ '.' + ss for ss in sL ]
        else: return [] # fail
    # Not in hash
    if c == '.':
        sL = get_valid_strings(s[1:], nums, in_hash, lev=lev+1)
        # print(f"{pad}recursion returned {sL}")
        if len(sL) : 
            return [ '.' + ss for ss in sL ]
        else : return []
    if c == '#':
        nums[0] = n-1
        sL = get_valid_strings(s[1:], nums, in_hash=True, lev=lev+1)
        if len(sL) : 
            return [ '#' + ss for ss in sL ]
        return [] # fail
    # c is '?' - try both
    # first assume its a '.'
    s_dot = get_valid_strings(s[1:], nums[:], in_hash, lev=lev+1)
    s1 = [ '.' + ss for ss in s_dot ]
    nums[0] = n-1
    s_hash = get_valid_strings(s[1:], nums, in_hash=True, lev=lev+1)
    # print(f"{pad}recursion returned {s_hash}")
    s2 = [ '#' + ss for ss in s_hash ]
    # print(f"{pad}s1 is {s1}  s2 is {s2}   ")
    s1.extend(s2)
    return s1



#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

reps = get_reports(db) # list of tuple ( orig_string, seq_ID)
#s = '.##.#...#..........##.....#........#......#....'
#print(f"{s} -> {get_sequence_from_good_string(s)}")


tot = 0
for r in reps:
    # r = ( '????..????.?????.????', [1,1,1,1])
    print(f"Working on {r}")
    sL = get_valid_strings(r[0], r[1])
    print(f" -- {len(sL)} valids for {r}")
    if sL: tot = tot + len(sL)
    # break
print(f"tot is {tot}")