import os
import sys
import itertools

class Case:
    def __init__(self, expected, numbers):
        self.expected = expected
        self.numbers = numbers

    def __iter__(self):
        return iter(self.numbers)
    
    def __len__(self):
        return len(self.numbers)

    @classmethod
    def from_line(cls, line):
        line = line.strip()
        expected, rest = line.split(":")
        expected = int(expected)
        rest = rest.strip()
        numbers = rest.split(" ")
        numbers = list(map(int, numbers))
        return cls(expected, numbers)
    
    def __str__(self):
        numbers = map(str, self.numbers)
        numbers = ' '.join(numbers)
        return f"{self.expected}: {numbers}"

def check_match(case, combinations):
    for combination in combinations:
        print(f"checking {combination} ", end='')
        result, *numbers = case.numbers
        for op, num in zip(combination, numbers):
            if op == "+":
                result += num
            else:
                result *= num
        print(result)
        if result == case.expected:
            return True
    return False
        
def partA(content):
    cases = map(Case.from_line, content.split("\n"))
    result = 0
    for c in cases:
        print(c)
        combinations = list(itertools.product("+*", repeat=len(c)-1)) + list(itertools.product("*+", repeat=len(c)-1))
        if check_match(c, combinations):
            result += c.expected

    print(result)

def checkB(expected: int, numbers: list[int]):
    cases = itertools.product('*|+', repeat=len(numbers)-1)
    for case in cases:
        result, *nums = numbers
        for op, num in zip(case, nums):
            if op == "*":
                result *= num
            if op == "+":
                result += num
            if op == "|":
                result = int(str(result) + str(num))
        if result == expected:
            return True
    return False

def partB(content):
    result = 0
    for line in content.split('\n'):
        print(line.split(" "))
        expected, *numbers = line.strip().split(" ")
        expected = expected.strip(":")
        expected = int(expected)
        numbers = list(map(int, numbers))
        print(numbers)
        if checkB(expected, numbers):
            result += expected
    
    print(result)
    return 0


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

