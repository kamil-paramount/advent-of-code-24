import os
import sys
from collections import Counter

from copy import deepcopy

def main():
    if len(sys.argv) != 2:
        print("python3 solve.py <file>")
        return 

    filename = sys.argv[1]
    print(f"Reading file {filename}")

    with open(filename, "r") as file:
        line_num = 0
        array_a = []
        array_b = []
        while line := file.readline().strip():
            x, y = map(int, line.split('   '))
            array_a.append((x, line_num))
            array_b.append((y, line_num))
            line_num += 1

    array_a.sort()
    array_b.sort()
    print(array_a)
    print(array_b)

    indexes = map(lambda e: (e[0][0], e[1][0]), zip(array_a, array_b))
    indexes = map(sorted, indexes)
    result = sum(map(lambda t: t[1] - t[0], indexes))
    print(result)

    arrA = list(map(lambda t: t[0], array_a))
    arrB = list(map(lambda t: t[0], array_b))

    counter = Counter(arrB)

    result = sum(map(lambda i: i * counter[i], arrA))
    print(f"RESULT 2: {result}")

if __name__ == "__main__":
    main()

