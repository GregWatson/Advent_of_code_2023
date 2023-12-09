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

class Hand:
    def __init__(self, hand, bid):
        self.hand = hand # string
        self.bid = bid # int
        self.type = None
        self.hex_hand = ''
        self.j_count = 0
        for i, c in enumerate(hand):
            new_c = c
            if c in 'TJQKA':
                if c == 'T': 
                    new_c = 'A'
                elif c == 'J': 
                    new_c = '1'
                elif c == 'Q': 
                    new_c = 'C'
                elif c == 'K': 
                    new_c = 'D'
                elif c == 'A': 
                    new_c = 'E'
            self.hex_hand = self.hex_hand + new_c

    # Has side effect of setting self.j_count - count of "jacks or jokers"
    def get_type(self):
        hand = self.hand
        # print(f"get type for hand {hand}")
        card_count = { }
        j_count  = 0
        for card in hand:
            if card == 'J':
                j_count = j_count + 1
                continue
            if card in card_count:
                card_count[card] = card_count[card]+1
            else:
                card_count[card] = 1
        self.j_count = j_count
        # print(f"{card_count}")
        t = 'high_card'
        saw_pair = False
        saw_three = False
        for c in card_count:
            if card_count[c] == 2:
                if saw_pair: t = 'two_pair'
                elif saw_three: t = 'full_house'
                else: 
                    t = 'one_pair'
                    saw_pair = True
                continue
            if card_count[c] == 3:
                if saw_pair: t = 'full_house'
                else : t = 'three'
                saw_three = True
                continue
            if card_count[c] == 4:
                t = 'four'
                continue
            if card_count[c] == 5: 
                t = 'five'
        return t

    def fix_jokers(self):
        j_count = self.j_count
        if not j_count: return
        # print(f"{self.hand} J count is {self.j_count}")
        t = self.type
        if j_count == 1:
            if t == 'high_card': self.type = 'one_pair'
            elif t == 'one_pair': self.type = 'three'
            elif t == 'two_pair': self.type = 'full_house'
            elif t == 'three': self.type = 'four'
            elif t == 'full_house': sys.exit(1) # cannot happen
            elif t == 'four': self.type = 'five'
            elif t == 'five': sys.exit(1) # cannot happen
            return
        if j_count == 2:
            if t == 'high_card': self.type = 'three'
            elif t == 'one_pair': self.type = 'four'
            elif t == 'two_pair': sys.exit(1) # cannot happen
            elif t == 'three': self.type = 'five'
            elif t == 'full_house': sys.exit(1) # cannot happen
            elif t == 'four': sys.exit(1) # cannot happen
            elif t == 'five': sys.exit(1) # cannot happen
            return
        if j_count == 3:
            if t == 'high_card': self.type = 'four'
            elif t == 'one_pair': self.type = 'five'
            else : sys.exit(1) # cannot happen
            return
        if j_count >= 4:
            if t == 'high_card': self.type = 'five'
            else : sys.exit(1) # cannot happen
            return

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

def sort_fun(h_obj):
    return h_obj.hex_hand

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

hands = []
for l in db:
    (hand,bid) = l.split()
    h = Hand(hand,int(bid))
    hands.append(h)

hands_by_type = {}
for t in types:
    hands_by_type[t] = []

for h in hands:
    h.type = h.get_type()

for h in hands:
    orig_t = h.type
    h.fix_jokers()
    if (h.type != orig_t):
        print(f"{h.hand} {orig_t}->{h.type} {h.j_count} {h.hex_hand}")
    hands_by_type[h.type].append(h)

# Sort them
for t in types: 
    hands_by_type[t].sort(key=sort_fun)

# for t in types: print(f"{t} {len(hands_by_type[t])}")
print("------------\n")
for h in hands_by_type['five']: print(f"{h.hand} {orig_t}->{h.type} {h.j_count} {h.hex_hand}")

sum = 0
pos = 1
for t in types: 
    for h in hands_by_type[t]:
        score = pos * h.bid
        sum = sum + score
        pos = pos + 1
print(f"{sum}")