import os
import sys
from collections import Counter

from copy import deepcopy

class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.north = self.south = self.east = self.west = None

    def name(self):
        return f"Node{self.x}{self.y}"

    def __str__(self):
        return (
            f"{self}:\n"
            f"  ↑ {self.north}"
            f"  ↓ {self.south}"
            f"  → {self.east}"
            f"  ← {self.west}"
        )

class Searcher:
    def __init__(self, nodes):
        self._nodes = nodes
    
    def same_as(self, val, coordinate):
        i = 0 if coordinate == 'x' else 1
        self._nodes = list(filter(lambda n: n[i] == val, self._nodes))
        return self

    def higher(self, val, coordinate):
        i = 0 if coordinate == 'x' else 1
        self._nodes = list(filter(lambda n: n[i] > val, self._nodes))
        return self
    
    def lower(self, val, coordinate):
        i = 0 if coordinate == 'x' else 1
        self._nodes = list(filter(lambda n: n[i] < val, self._nodes))
        return self

    def highest(self, coordinate):
        if not self._nodes:
            return None
        
        i = 0 if coordinate == 'x' else 1
        nodes = list(self._nodes)
        result = nodes[0]
        for n in nodes[1:]:
            if n[i] > result[i]:
                result = n
        return result

    def lowest (self, coordinate):
        if not self._nodes:
            return None
        
        i = 0 if coordinate == 'x' else 1
        nodes = list(self._nodes)
        result = nodes[0]
        for n in nodes[1:]:
            if n[i] < result[i]:
                result = n
        return result


class Board:
    def __init__(self, raw):
        self._board = []
        lines = raw.split('\n')
        for y, line in enumerate(lines):
            board_line = []
            self._board.append(board_line)
            for x, ch in enumerate(line):
                if ch == "^":
                    self.initial_guard_position = (y, x)
                    board_line.append("X")
                    continue
                board_line.append(ch)
    
    def add(self, x, y):
        self._obstacles.add((x, y))
    
    def __str__(self):
        lines = []
        for line in self._board:
            lines.append(''.join(line))
        return '\n'.join(lines)

    def get(self, pos):
        if pos[0] < 0 or pos[1] < 0:
            return None
        try:
            return self._board[pos[0]][pos[1]]
        except IndexError:
            return None

    def visit(self, pos):
        self._board[pos[0]][pos[1]] = "X"

    def get_visited(self):
        visited = 0
        for line in self._board:
            for pos in line:
                if pos == "X":
                    visited += 1
        return visited

    def get_obstacle_positions(self):
        result = set()
        for x, line in enumerate(self._board):
            for y, ch in enumerate(line):
                node = (x, y)
                if node == self.initial_guard_position:
                    continue
                if ch != "X":
                    continue
                result.add(node)
        return result

    def get_cleared_board(self):
        board = deepcopy(self._board)
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == 'X':
                    board[x][y] = '.'
        guard_pos = self.initial_guard_position
        board[guard_pos[0]][guard_pos[1]] = "X"
        return board

class LimitedBoard(Board):
    def __init__(self, board):
        self._board = board
        self.size = (len(board), len(board[0]))
        self.steps = self.size[0] * self.size[1]
    
    def check_loop(self, guard):
        self.initial_guard_position = guard.x, guard.y
        while True:
            if self.steps < 0:
                return True
            next_pos = guard.get_next_pos()
            next_board = self.get(next_pos)
            if next_board is None:
                return False
            if next_board == "#":
                guard.rotate()
            else:
                self.steps -= 1
                guard.move()
                self.visit(next_pos)

class Guard:
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

    def get_next_pos(self):
        if self.direction == "north":
            return (self.x-1, self.y)
        if self.direction == "south":
            return (self.x+1, self.y)
        if self.direction == "east":
            return (self.x, self.y+1)
        if self.direction == "west":
            return (self.x, self.y-1)

    def move(self):
        self.x, self.y = self.get_next_pos()

    def __str__(self):
        directions = {
            "north": "↑",
            "south": "↓",
            "east": "→",
            "west": "←",
        }
        return f"G({self.x}, {self.y}) {directions[self.direction]}"

    def rotate(self):
        rotation_map = {
            "north": "east",
            "east": "south",
            "south": "west",
            "west": "north",
        }
        self.direction = rotation_map[self.direction]

    def as_tuple(self):
        return (self.x, self.y)

def stageA(board, guard):
    while True:
        next_pos = guard.get_next_pos()
        next_board = board.get(next_pos)
        if next_board is None:
            break
        if next_board == "#":
            guard.rotate()
        else:
            guard.move()
            board.visit(next_pos)

    print(board.get_visited())

def stageB(board, guard):
    print("solving the board")
    while True:
        next_pos = guard.get_next_pos()
        next_board = board.get(next_pos)
        if next_board is None:
            break
        if next_board == "#":
            guard.rotate()
        else:
            guard.move()
            board.visit(next_pos)
    
    print("Getting potential positions")
    obstacle_positions = board.get_obstacle_positions()
    print(obstacle_positions)

    cleared_board = board.get_cleared_board()
    # print(cleared_board)
    boards = []
    for pos in obstacle_positions:
        copied_board = deepcopy(cleared_board)
        current_val = copied_board[pos[0]][pos[1]]
        if current_val == "#":
            raise Exception(pos)
        copied_board[pos[0]][pos[1]] = "#"
        b = LimitedBoard(copied_board)
        boards.append(b)
    
    loops = 0
    for i, b in enumerate(boards):
        print(f"Solving board {i}")
        g_x, g_y = board.initial_guard_position
        g = Guard(g_x, g_y, "north")
        is_loop = b.check_loop(g)
        if is_loop:
            loops += 1

    print(loops)

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

    board = Board(content)
    guard_pos = board.initial_guard_position
    guard = Guard(guard_pos[0], guard_pos[1], "north")

    if stage == 'a':
        stageA(board, guard)
    else:
        stageB(board, guard)

if __name__ == "__main__":
    main()

