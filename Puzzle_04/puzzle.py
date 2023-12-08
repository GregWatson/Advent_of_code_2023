#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
syms = ( r'*-%+/@&#$=' )
patt = re.compile("Card\s+(\d+):\s*([^|]*)\|\s*(.*)")

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

def get_cards(db):
    cards = []
    for l in db:
        m = patt.match(l)
        if m:
            card_id = int(m.group(1))
            win_text = m.group(2)
            my_nums_text = m.group(3)
            win_nums_txt_list = win_text.split()
            my_nums_text_list = my_nums_text.split()
            # print(f'Card {card_id} win: {win_nums_txt_list}  mine: {my_nums_text_list}')
            wins = [int(i) for i in win_nums_txt_list]
            mine = [ int(i) for i in my_nums_text_list]
            cards.append((card_id, wins,mine))
        else:
            print(f"Error - didn't matych line {l}")
    return cards

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print(f"Read {len(db)} words from {input_file_name}. Line length is {len(db[0])}")

cards  = get_cards(db)

# c is list of ( num_wins, num_cards)
c = [ [0,0] for i in range(len(db)+1)]

sum = 0
for (card_id, wins, mine) in cards:
    power = 0
    c[card_id][1] = 1
    for m in mine:
        if m in wins:
            power = 1 if power == 0 else power * 2
            c[card_id][0] = c[card_id][0]+1
    sum = sum + power
print(f'sum is {sum}')

tot_cards = 0
for id in range(len(db)+1):
    num_wins = c[id][0]
    num_cards = c[id][1]
    tot_cards = tot_cards + num_cards
    print(f'card id {id} has {num_wins} and we have {num_cards} of them. Tot is {tot_cards}')
    if num_wins > 0:
        for cc in range(num_cards):
            for i in range(num_wins):
                c[id+i+1][1] = c[id+i+1][1]+1
print(f'Tot cards is {tot_cards}')