import os
import sys
from collections import Counter

from copy import deepcopy

def as_diffs(report):
    differences = list(map(lambda t: t[0] - t[1], zip(report, report[1:])))

    if differences[0] < 0:
        differences = list(map(lambda x: x * -1, differences))
    
    return differences

def is_report_safe(report):
    diffs = as_diffs(report)
    for d in diffs:
        if not 0 < d < 4:
            return False
    
    return True

def stageA(data):
    safe_report = 0
    for report in data:
        if is_report_safe(report):
          safe_report += 1

    print(safe_report)

def stageB(data):
    safe_report = 0
    for report in data:
        print()
        print(f"Report: {report} ", end='')
        if is_report_safe(report):
            safe_report += 1
            print("OK")
            continue

        print(f"NEEDS CHECK")

        reports_to_check = [
            report[:i]+report[i+1:]
            for i in range(len(report))
        ]
        for r in reports_to_check:
            print(f"Report: {report}", end=" ")
            if is_report_safe(r):
                safe_report += 1
                print("OK")
                break
            print("FALSE")
    print(safe_report)

def main():
    argc = len(sys.argv)
    if argc > 3 or argc < 2:
        print("python3 solve.py <file> <stage>")
        return 

    filename = sys.argv[1]
    stage = sys.argv[2].lower() if argc == 3 else 'a'
    if not stage in ['a', 'b']:
        print("unrecognized stage")

    data = []
    with open(filename, "r") as file:
        while line := file.readline().strip():
            report = list(map(int, line.split(" ")))
            data.append(report)


    if stage == 'a':
        stageA(data)
    else:
        stageB(data)

if __name__ == "__main__":
    main()

