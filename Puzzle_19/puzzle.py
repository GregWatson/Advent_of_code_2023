#import argparse
import sys
import re
import functools
import array
import copy



class Part:
    def __init__(self,x,m,a,s):
        self.x=x
        self.m=m
        self.a=a
        self.s=s

    def print(self):
        print(f"X:{self.x} M:{self.m} A:{self.a} S:{self.s}")

    def get_val(self, letter):
        return self.x if letter  == 'x' else self.m if letter == 'm' else self.a if letter == 'a' else self.s
    
    def rating_sum(self):
        return self.x + self.m + self.a +self.s

def load_rules():
    rules = {}
    with open("rules.txt") as f:
        lines = f.readlines()
    rules_txt = [ l.strip() for l in lines ]
    for r in rules_txt:
        m = re.match(r'([a-z]+)\{([^}]+)\}', r)
        if m:
            rule_ID = m.group(1)
            if len(rule_ID) <2 or len(rule_ID) > 3:
                print(f"SAW rule ID {rule_ID}")
            seqL = m.group(2).split(',')
            # print(f"{rule_ID} -> {seqL}")
            rules[rule_ID] = seqL
    return rules

def load_parts():
    parts = []
    with open("parts.txt") as f:
        lines = f.readlines()
    parts_txt = [ l.strip() for l in lines ]
    for pl in parts_txt:
        m = re.match(r'\{x=(\d+),m=(\d+),a=(\d+),s=(\d+)\}', pl)
        if m:
            p = Part(int(m.group(1)),int(m.group(2)), int(m.group(3)), int(m.group(4)) )
            # p.print()
            parts.append(p)
    return parts



def load_db():
    with open(input_file_name) as f:
        lines = f.readlines()
    return [ l.strip() for l in lines ]

def process_rule(rule,p):
    # returns A, R, rule_id or 'c'. 'c' means try next rule
    colon_pos = rule.find(':')
    target_rule = rule[colon_pos+1:]
    letter = rule[0] # one of xmas
    value = p.get_val(letter)
    relop = rule[1]
    comparand = int(rule[2:colon_pos])
    # print(f"       Rule {rule} is IF {letter}(value {value}) {relop} {comparand} THEN {target_rule}")
    if relop == '<':
        if value < comparand:
            return target_rule
        return 'c'
    if value > comparand:
        return target_rule
    return 'c'



def process_part(p, rules):
    rule_id = 'in'
    print(f"Process part ",end='')
    p.print()
    while rule_id:
        print(f"   rule_id {rule_id}")
        rule_seq = rules[rule_id]
        for rule in rule_seq:
            if len(rule) < 4: # unconditional rule
                if rule == 'A': return True
                if rule == 'R': return False
                rule_id = rule
                break
            else: # conditional rule
                next = process_rule(rule, p)
                if next == 'c': continue
                if next == 'A' : return True
                if next == 'R' : return False
                rule_id = next
                break




#---------------------------------------------------------------------------------------
# Load input
rules = load_rules()
parts = load_parts()
print(f"Saw {len(rules)} rules and {len(parts)} parts ")

c = 0
for p in parts:
    res = process_part(p, rules)
    if res:
        c = c + p.rating_sum()

print(f"Total is {c}")
