import os
import sys
from collections import defaultdict

from copy import deepcopy

class RulesGuard:
    def __init__(self):
        self.rules = defaultdict(set)

    def add_rule(self, x, y):
        self.rules[y].add(x)

    def get_solver(self):
        return Solver(deepcopy(self.rules))

    def __str__(self):
        return str(self.rules)

class Solver:
    def __init__(self, rules):
        self.rules = rules

    def intersect_data(self, case):
        pages = set(case)
        for v in self.rules.values():
            v.intersection_update(pages)

    def solve(self, case: list[int]):
        # print(f"Solving case: {case}")
        self.intersect_data(case)
        for page in case:
            # print(f"Handlingj page {page}")
            page_rules = self.rules[page]
            # print(f"Needs to be after: {page_rules}")
            if len(page_rules) >= 1:
                return False
            for v in self.rules.values():
                v.discard(page)

        return True

    def correct(self, case):
        print(f"Correcting: {case}")
        self.intersect_data(case)
        pages_num = len(case)
        pages = set(case)
        solution = []

        filtered_data = {
            k: v
            for k, v in self.rules.items()
            if k in pages
        }
        for page in pages:
            if page not in filtered_data:
                filtered_data[page] = set()

        print(f"Filtered data: {filtered_data}")

        while len(filtered_data) > 0:
            candidate = None

            for k, v in filtered_data.items():
                if len(v) == 0:
                    candidate = k
                    break

            if candidate is None:
                raise Exception("No candidate found")
            
            solution.append(candidate)
            for v in filtered_data.values():
                v.discard(candidate)
            del filtered_data[candidate]

        print(f"Corrected: {solution}")
        return solution

def fix_ordering(case, guard):
    solver = guard.get_solver()
    return solver.correct(case)

def main():
    if len(sys.argv) != 2:
        print("python3 solve.py <file>")
        return 

    filename = sys.argv[1]
    print(f"Reading file {filename}")

    guard = RulesGuard()
    with open(filename, "r") as file:
        while line := file.readline().strip():
            x, y = map(int, line.split('|'))
            guard.add_rule(x, y)

        correct_sum = 0
        incorrect_sum = 0
        while line := file.readline().strip():
            case = list(map(int, line.split(',')))
            solver = guard.get_solver()
            result = solver.solve(case)
            print(case, result)
            if not result:
                fixed_ordering = fix_ordering(case, guard)
                incorrect_sum += fixed_ordering[len(case) // 2]
                continue

            correct_sum += case[len(case) // 2]
    
    print(f"Correct sum: {correct_sum}")
    print(f"Incorrect sum: {incorrect_sum}")

if __name__ == "__main__":
    main()

