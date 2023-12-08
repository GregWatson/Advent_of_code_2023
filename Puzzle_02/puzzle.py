#import argparse
import sys
import re

input_file_name = 'input.txt'
debug = True
DIGITS = ("zero","one","two","three","four","five","six","seven","eight","nine")

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

def parse_line(l):
    # return game_ID and max r,g,b seen
    max_seen = { 'red': 0, "green":0, "blue":0 }
    m = re.match(r"Game (\d+): (.*)", l,)
    if m:
        game_id = int(m.group(1))
        tries = m.group(2).split("; ")  # each try has one or more of red green blue count.
        for t in tries:
            counts = t.split(", ") # list of up to 3 counts. e.g. "4 red" or "12 blue"
            for c in counts:
                m1 = re.match(r"(\d+) (red|green|blue)", c)
                if m1:
                    num_seen = int(m1.group(1))
                    color = m1.group(2)
                    if num_seen > max_seen[color]:
                        max_seen[color] = num_seen
                else:
                    print("ERROR: unknown color count format:" + c)

    else:
        print("Regex failed to parse input line " + l)
    return (game_id, max_seen)
    

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print("Read {} words from {}.".format(len(db), input_file_name))
sum=0
power_sum=0

for l in db:
    (game_id,rgb_max) = parse_line(l)
    # print("Game {} = {}".format(game_id, rgb_max))
    if ( (rgb_max['red']<=12) and (rgb_max['green']<=13) and rgb_max['blue']<=14):
        sum = sum + game_id
    power = rgb_max['red'] * rgb_max['green'] * rgb_max['blue']
    power_sum = power_sum + power
    print("Game ID {} has power {}".format(game_id,power))

print("Sum is ", sum)
print("Power Sum is ", power_sum)