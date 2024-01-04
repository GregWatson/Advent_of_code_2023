#import argparse
import sys
import re
import functools
import array
import copy

input_file_name = 'input.txt'
L=0
R=1
U=2
D=3
grid = None
x_max = 0
y_max= 0
MAX = 1000000
lc = None

class State:
    def __init__(self, x=0,y=0, dir=L, stepsMade=0, loss = 0):
        self.x=x
        self.y=y
        self.dir=dir
        self.stepsMade = stepsMade
        self.loss = loss

def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def get_input_grid(db):
    grid = []
    for l in db:
        grid.append( array.array('b',map( lambda x: int(x), list(l))))
    return grid

def print_grid(g):
    x_max = len(g[0])
    y_max = len(g)
    for y in range(y_max):
        for x in range(x_max):
            print(f"{g[y][x]}", end='')
        print("")
    print("\n")

def print_States(S):
    for st in S:
        print(f"{st.x},{st.y} L={st.loss}  D={st.dir} steps={st.stepsMade}")


def check_state(S, s):
    global grid
    global x_max
    global y_max
    global lc
    # check bounds.
    if s.x < 0 or s.x >= x_max or s.y < 0 or s.y >= y_max: 
        return
    # If this is the lowest loss to this x,y then add it to S
    lossToHere = s.loss + grid[s.y][s.x]
    curr_lc = lc[s.x][s.y][s.dir][s.stepsMade]
    if lossToHere < curr_lc:
        lc[s.x][s.y][s.dir][s.stepsMade] = lossToHere
        s.loss = lossToHere
        print(f"   Current mac at {s.x},{s.y} was {curr_lc}. Now set to {lossToHere}")
        # Add state at sorted location in S
        for i,Ss in enumerate(S):
            if lossToHere < Ss.loss:
                S.insert(i, s)
                break
        else:
            S.append(s)

        print(f"After adding State at {s.x},{s.y} with loss {lossToHere}, full state list is")
        print_States(S)
    else:
        print(f"   Current mac at {s.x},{s.y} was {curr_lc} which is lower than {lossToHere} so discarding this state")







def find_shortest_path(S, to_x, to_y):
    while len(S):
        s = S.pop(0)
        if s.x == to_x and s.y == to_y:
            return s.loss
        # try dirs. Never go back to immediately prev space.
        print(f"Starting from ({s.x},{s.y})")
        # try down (D)
        if s.dir != U and not (s.dir == D and s.stepsMade == 3):
            newStepsMade = 1 if s.dir != D else s.stepsMade+1
            check_state(S, State(s.x, s.y+1, D, newStepsMade, s.loss))




#---------------------------------------------------------------------------------------
# Load input
db = load_db()

#print(f"{db}")
x_max = len(db[0])
y_max = len(db)
print(f"Read {y_max} lines from {input_file_name}. First Line length is {x_max}.")

grid = get_input_grid(db)

# create lowest cost array. [x][y][dir][numSteps]
lc = [ ]
for y in range(y_max):
    xl = [ [ [MAX, MAX, MAX, MAX], 
             [MAX, MAX, MAX, MAX],
             [MAX, MAX, MAX, MAX],
             [MAX, MAX, MAX, MAX] 
    ] for x in range(x_max) ]
    lc.append(xl)

#print_grid(grid)

activeStates = []
activeStates.append(State(1,0,R,1,5))
activeStates.append(State(0,1,D,1,5))

print_States(activeStates)

shortestPathLoss = find_shortest_path(activeStates, x_max-1, y_max-1)
print(f"Loss is {shortestPathLoss}")