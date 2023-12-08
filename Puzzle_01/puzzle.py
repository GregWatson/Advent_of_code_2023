import argparse
import sys

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


# Get first and last numbers that are digits. 
# Return 10*first+first if only one number is found.
def get_num_from_line(l):
    first_digit=None
    last_digit=None
    for c in l:
        if c.isdigit():
            number = int(c)
            if first_digit is None:
                first_digit = number
            else:
                last_digit=number
    if last_digit==None:
        return 10*first_digit + first_digit
    return 10*first_digit + last_digit

# Replace written numbers by their value.
def repl_textual_numbers(l):
    new=""
    pos=0  # current first char we are considering
    while pos < len(l):
        if l[pos:pos+1].isdigit(): # just keep it and move on
            c = l[pos:pos+1]
            new = new + c
            pos = pos+1
            #print(''+l+' has digit ' + c)
        else: # check for digit in text form
            matched=False
            for dig_val,s in enumerate(DIGITS):
                dig_len = len(s)
                if l[pos:pos+dig_len] == s:
                    matched=True
                    new = new + str(dig_val)
                    pos = pos + dig_len - 1 # Need to keep last char in case of an overlap-
                    break
            if not matched:
                pos=pos+1
    return new

#---------------------------------------------------------------------------------------
# Load input
db = load_db()
if debug: print("Read {} words from {}.".format(len(db), input_file_name))
sum=0

for l in db:
    newl = repl_textual_numbers(l)
    number=get_num_from_line(newl)
    sum = sum + number
    print("%s becomes %s and number is %d so running sum is %d" % (l, newl,number, sum))
print("Sum is ", sum)