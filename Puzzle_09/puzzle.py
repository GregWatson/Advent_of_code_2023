#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )
#seeds_patt = re.compile("seeds: (.*)")
#map_name_patt = re.compile("([a-z-]+) map:.*")
#range_patt = re.compile(r"(\d+)\s*(\d+)\s*(\d+)")
types = [ 'high_card', 'one_pair', 'two_pair', 'three', 'full_house', 'four', 'five']


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

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

sum=0
neg_sum =0
for l in db:
    strs = l.split() # all the sequences, each getting 1 shorter than previous
    seqs = [ [int(i) for i in strs] ] # convert to ints
    done = False
    seq_id = 0
    while not done:
        print(f"{seq_id} - {seqs[seq_id]}")
        newl = []
        for i in range(len(seqs[seq_id])-1): 
            newl.append(seqs[seq_id][i+1]-seqs[seq_id][i])
        for i in newl:
            if i != 0 : 
                seq_id = seq_id + 1
                seqs.append(newl)
                break
        else:
            done = True

    # add last num to prev list
    n = seqs[-1][0]
    for seq_id in range(len(seqs)-2,-1,-1) :
        print(f"seq_id {seq_id}")
        seqs[seq_id].append(seqs[seq_id][-1]+ seqs[seq_id+1][-1])
        n = seqs[seq_id][0] - n

    neg_sum = neg_sum + n
    sum = sum + seqs[0][-1]
    print(f"n:{n}   sum:{sum} neg_sum:{neg_sum}")

