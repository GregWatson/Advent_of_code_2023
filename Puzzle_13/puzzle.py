#import argparse
import sys
import re
import functools
import array

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

def get_patterns(db):
    pL = []
    p = [] # current pattern    
    for l in db:
        if len(l): p.append(l)
        else:
            if len(p): pL.append(p)
            p = []
    if len(p): pL.append(p)
    return pL

# check that row i,i+1 of p are indeed a mirror
def check_mirror(p, i):
    l = len(p)
    t = i-1
    b = i+2
    while t >= 0 and b < l:
        if p[t] != p[b]: return False
        t=t-1
        b=b+1
    return True

# return the location of all horiz mirror position.
# Mirror lies between pos and pos+1
def get_horiz_mirror_pos(p, orig_pos=-1):
    L = []
    for i, l in enumerate(p[:-1]):
        if i == orig_pos:
            continue
        if l == p[i+1]:
            if check_mirror(p, i):
                L.append(i)
    return L

def p_print(p):
    return "\n".join(p)

def get_transpose(p):
    r = []
    for x in range(len(p[0])):
        s = ''
        for y in p:
            s = s + y[x]
        r.append(s)

    # print(f"Transp of\n{p_print(p)}\nis\n{p_print(r)}")
    return r


# smudge pattern and get return the location of all horiz mirror position.
# Mirror lies between pos and pos+1
def get_smudged_horiz_mirror_pos(p, orig_pos):
    tmp = p[:]
    length = len(p[0])
    L = []
    # if > 2 diffs then cannot smudge to success
    for i,l in enumerate(tmp):
        row = array.array('u',l)
        # print(f"{row}")
        for x in range(length):
            if row[x] == '#': row[x] = '.'
            else: row[x] = '#'
            tmp[i] = ''.join(row)
            R = get_horiz_mirror_pos(tmp, orig_pos=orig_pos)
            if len(R) : print(f"Smudge at row{i} pos{x} - gave results {R}")
            for r in R:
                if r != orig_pos and not r in L:
                    print(f"-- smudge soln is {r}")
                    L.append(r)
            #restore row
            if row[x] == '#': row[x] = '.'
            else: row[x] = '#'
        tmp[i] = p[i]
    return L



#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

pL = get_patterns(db)

orig_horiz_soln = []
orig_vert_soln = []
tot = 0
for i, p in enumerate(pL):
    # r = ( '.....????..????.?????.????', [1,1,1,1])
    print(f"Line {i} : Working on \n{p_print(p)}")
    print(f"--------------------------\n")
    L = get_horiz_mirror_pos(p)
    if len(L) > 1 : print(f"<<< MULTI H MIRROR >>>")
    if not len(L) : orig_horiz_soln.append(-1)
    else:
        for i in L:
            h_lines_above = i+1
            tot = tot + 100*h_lines_above
            if h_lines_above : print(f"\nh above: {h_lines_above}\n{p_print(p)}")
            orig_horiz_soln.append(i)

    # do vert check by transposing matrix and running horiz find on it.
    pT = get_transpose(p)
    L = get_horiz_mirror_pos(pT)
    if len(L) > 1 : print(f"<<< MULTI V MIRROR >>>")
    if not len(L) : orig_vert_soln.append(-1)
    else:
        for i in L:
            v_lines_left = i+1
            tot = tot + v_lines_left
            orig_vert_soln.append(i)

            if v_lines_left : print(f"\nv_left:{v_lines_left}\n1234567890\n{p_print(pT)}")

    print(f"tot = {tot}")

    # if h_lines_above and v_lines_left: print(f"**** BOTH ****")
print(f"tot is {tot}")

print(f"\nPart 2\n")

tot = 0
for i, p in enumerate(pL):
    # r = ( '.....????..????.?????.????', [1,1,1,1])
    print(f"Line {i} : Working on \n{p_print(p)}")
    print(f"--------------------------\n")
    L = get_smudged_horiz_mirror_pos(p, orig_horiz_soln[i])
    if len(L) > 1 : print(f"<<< MULTI H MIRROR >>>")
    seen_solution = 0
    for r in L:
        h_lines_above = r+1
        tot = tot + 100*h_lines_above
        if h_lines_above : print(f"\nh above: {h_lines_above}\n{p_print(p)}")
        seen_solution = seen_solution + 1

    # do vert check by transposing matrix and running horiz find on it.
    pT = get_transpose(p)
    print(f"Line {i} Transposed: Working on \n{p_print(pT)}")
    L = get_smudged_horiz_mirror_pos(pT, orig_vert_soln[i])
    if len(L) > 1 : print(f"<<< MULTI V MIRROR >>>")
    for r in L:
        v_lines_left = r+1
        tot = tot + v_lines_left
        seen_solution = seen_solution + 1

        if v_lines_left : print(f"\nv_left:{v_lines_left}\n1234567890\n{p_print(pT)}")

    if seen_solution == 0: 
        print("----  No solutions found!!!!  ------")
        sys.exit(1)
    print(f"tot = {tot}")

    # if h_lines_above and v_lines_left: print(f"**** BOTH ****")
print(f"tot is {tot}")

