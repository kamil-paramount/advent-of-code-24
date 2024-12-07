import os
import sys

import re

class Cell:
    def __init__(self, x, y, char, board):
        self.x = x
        self.y = y
        self.char = char
        self.part_of_xmas = False
        self.board = board
    
    def get_rel(self, x, y):
        return self.board.get(self.x + x, self.y + y)

    def get_position(self):
        return self.x, self.y

    def mark(self):
        self.part_of_xmas = True
    
    def matches(self, ch):
        return self.char == ch
    
    def is_m_or_s(self):
        return self.char == 'M' or self.char == 'S'
    
    def is_other_than(self, other):
        return self.char != other.char

    def __repr__(self):
        return f'<Cell({self.x}, {self.y}, {self.char})>'

    def __str__(self):
        if not self.part_of_xmas:
            return '.'
        return self.char

class Board:
    def __init__(self, content):
        self._data = []
        lines = content.split("\n")
        for x, row in enumerate(lines):
            data_row = []
            for y, char in enumerate(row):
                data_row.append(Cell(x, y, char, self))
            self._data.append(data_row)
    
    def __str__(self):
        result = ''
        for row in self._data:
            for cell in row:
                result += str(cell)
            result += '\n'
        
        return result

    def get(self, x, y):
        last_cell = self._data[-1][-1]
        max_x, max_y = last_cell.get_position()
        if x < 0 or y < 0:
            raise IndexError("negative index")
        
        if x > max_x or y > max_y:
            raise IndexError(f"({x}, {y}) out of board")
        
        return self._data[x][y]

    def __iter__(self):
        def iter():
            for row in self._data:
                for cell in row:
                    yield cell
            
        return iter()


def check_cell(cell):
    increments = [
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, 1),
        (0, 1),
        (0, -1),
        (1, -1),
        (-1, -1),
    ]
    total_xmases = 0

    print(f"Checking {repr(cell)}")
    for inc_x, inc_y in increments:
        print(f"Increment: {inc_x}, {inc_y} ", end='')
        for i, expected in enumerate("XMAS"):
            try:
                c = cell.get_rel(inc_x * i, inc_y * i)
                if not c.matches(expected):
                    # print(repr(c), expected)
                    break
            except IndexError as e:
                # print(e)
                break
        else:
            print("Matches", end="")
            for i in range(4):
                c = cell.get_rel(inc_x * i, inc_y * i)
                c.mark()
                # print(repr(c))
                
            total_xmases += 1
        print()

    print()
    return total_xmases

def check_cross(cell):
    positions = [
        (-1, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
    ]

    try:
        cells = list(
            map(
                lambda p: cell.get_rel(p[0],p[1]),
                positions
            )
        )
    except IndexError:
        return 0
    
    for c in cells:
        if not c.is_m_or_s():
            return 0
    
    if (
        not cells[0].is_other_than(cells[1])
        or not cells[2].is_other_than(cells[3])
    ):
        return 0

    for c in cells:
        c.mark()

    cell.mark()

    return 1

def partA(content):
    board = Board(content)
    print(board)

    result = 0
    for cell in board:
        if not cell.matches('X'):
            continue
        result += check_cell(cell)

    print(board)
    print(result)

def partB(content):
    board = Board(content)
    print(board)

    result = 0
    for cell in board:
        if not cell.matches('A'):
            continue
        result += check_cross(cell)

    print(board)
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

