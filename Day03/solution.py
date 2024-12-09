import os
import sys

import re

pattern = r'mul\((?P<number_a>\d{1,3}),(?P<number_b>\d{1,3})\)'
pattern_do = (
    r'(?P<mul>mul\('
        r'(?P<number_a>\d{1,3}),'
        r'(?P<number_b>\d{1,3})'
    r'\))'
    r'|(?P<dont>don\'t\(\))'
    r'|(?P<do>do)'
)
def partA(content):
    matches = re.findall(pattern, content)
    multiplied = map(lambda t: int(t[0])*int(t[1]), matches)
    result = sum(multiplied)
    print(result)


def partB(content):
    matches = re.findall(pattern_do, content)
    do = True
    result = 0
    for m in matches:
        if m[3] == "don't()":
            do = False
            continue
        if m[4] == "do":
            do = True
            continue
        if do:
            print(m)
            result += int(m[1]) * int(m[2])

    print(result)

def main():
    argc = len(sys.argv)
    if argc > 3 or argc < 2:
        print("python3 solve.py <file> <stage>")
        return 

    filename = sys.argv[1]
    stage = sys.argv[2].lower() if argc == 3 else 'a'
    if not stage in ['a', 'b']:
        print("unrecognized stage")

    with open(filename, "r") as file:
        content = file.read()

    if stage == 'a':
        partA(content)
    else:
        partB(content)

if __name__ == "__main__":
    main()

