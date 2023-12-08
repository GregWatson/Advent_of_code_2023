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
        for i, c in enumerate(hand):
            new_c = c
            if c in 'TJQKA':
                if c == 'T': 
                    new_c = 'A'
                elif c == 'J': 
                    new_c = 'B'
                elif c == 'Q': 
                    new_c = 'C'
                elif c == 'K': 
                    new_c = 'D'
                elif c == 'A': 
                    new_c = 'E'
            self.hex_hand = self.hex_hand + new_c

    def get_type(self):
        hand = self.hand
        # print(f"get type for hand {hand}")
        card_count = { hand[0] : 1 }
        for card in hand[1:]:
            if card in card_count:
                card_count[card] = card_count[card]+1
            else:
                card_count[card] = 1
        # print(f"{card_count}")
        t = 'high_card'
        saw_pair = False
        saw_three = False
        for c in card_count:
            if card_count[c] == 2:
                if saw_pair: return 'two_pair'
                if saw_three: return 'full_house'
                t = 'one_pair'
                saw_pair = True
                continue
            if card_count[c] == 3:
                if saw_pair: return 'full_house'
                t = 'three'
                saw_three = True
            if card_count[c] == 4:
                return 'four'
            if card_count[c] == 5: 
                return 'five'
        return t

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
    if (h.type != 'none'):
        print(f"{h.hand} {h.type}")
    hands_by_type[h.type].append(h)

# for t in types: print(f"{t} {len(hands_by_type[t])}")

sum = 0
pos = 1
for t in types: 
    hands_by_type[t].sort(key=sort_fun)
    for h in hands_by_type[t]:
        score = pos * h.bid
        sum = sum + score
        pos = pos + 1
print(f"{sum}")