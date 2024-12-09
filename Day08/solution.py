import os
import sys
import itertools
from collections import defaultdict, namedtuple
from copy import copy

Point = namedtuple('Point', ['x', 'y'])

class Map:
    def __init__(self, size: Point):
        self.size = size
        self.antennas = defaultdict(set)
        self.nodes = set()

    def calc_b(self):
        result = copy(self.nodes)
        for antenna_set in self.antennas.values():
            if len(antenna_set) < 2:
                continue
            for antenna in antenna_set:
                result.add(antenna.pos)
        return len(result)


    def add_antenna(self, antenna):
        self.antennas[antenna.type].add(antenna)

    def all_antennas(self):
        for antenna_set in self.antennas.values():
            for a in antenna_set:
                yield a

    def values(self):
        return self.antennas.values()

    @classmethod
    def from_content(cls, content):
        lines = content.split("\n")
        x_size = len(lines)
        y_size = len(lines[0])

        m = Map(Point(x_size, y_size))
        for x, line in enumerate(lines):
            for y, char in enumerate(line):
                if char != '.':
                    antenna = Antenna(char, Point(x, y))
                    m.add_antenna(antenna)
        return m


    def __str__(self):
        lines = []
        for _ in range(self.size.x):
            line = []
            lines.append(line)
            for _ in range(self.size.y):
                line.append('.')
        
        for antenna in self.all_antennas():
            pos = antenna.pos
            lines[pos.x][pos.y] = antenna.type

        str_lines = map(''.join, lines)
        return '\n'.join(str_lines)

    def with_nodes(self):
        lines = []
        for _ in range(self.size.x):
            line = []
            lines.append(line)
            for _ in range(self.size.y):
                line.append('.')
        
        for antenna in self.all_antennas():
            pos = antenna.pos
            lines[pos.x][pos.y] = antenna.type

        for node in self.nodes:
            lines[node.x][node.y] = "#"

        str_lines = map(''.join, lines)
        return '\n'.join(str_lines)

    def add_node(self, rel_node: Point, from_antenna):
        node = Point(
            from_antenna.pos.x + rel_node.x,
            from_antenna.pos.y + rel_node.y,
        )
        return self.add_node_exact(node)
    
    def add_node_exact(self, node: Point):
        if node.x < 0 or node.y < 0:
            return False
        
        if node.x >= self.size.x or node.y >= self.size.y:
            return False

        self.nodes.add(node)
        return True

class Antenna:
    def __init__(self, type, pos: Point):
        self.type = type
        self.pos = pos
    
    def distance_to(self, other) -> Point:
        return Point(
            other.pos.x - self.pos.x,
            other.pos.y - self.pos.y,
        )

    def __str__(self):
        return f"<Antenna #{self.type} {self.pos}>"

def add_points(a: Point, b: Point) -> Point:
    return Point(a.x + b.x, a.y + b.y)

def partB(antenna_map):
    result = 0

    for antennas in antenna_map.values():
        pairs = itertools.combinations(antennas, r=2)
        for antenna_a, antenna_b in pairs:
            new_antenna = antenna_b.pos
            distance = antenna_a.distance_to(antenna_b)
            while True:
                new_node = add_points(new_antenna, distance)
                node_added = antenna_map.add_node_exact(new_node)
                if not node_added:
                    break
                new_antenna = new_node

            new_antenna = antenna_a.pos
            distance = antenna_b.distance_to(antenna_a)
            while True:
                new_node = add_points(new_antenna, distance)
                node_added = antenna_map.add_node_exact(new_node)
                if not node_added:
                    break
                new_antenna = new_node    

    print(antenna_map)
    print()
    print(antenna_map.with_nodes())

    print(antenna_map.calc_b())

def partA(antenna_map):
    for antennas in antenna_map.values():
        pairs = itertools.combinations(antennas, r=2)
        for antenna_a, antenna_b in pairs:
            distance = antenna_a.distance_to(antenna_b)
            antenna_map.add_node(distance, antenna_b)

            distance = antenna_b.distance_to(antenna_a)
            antenna_map.add_node(distance, antenna_a)

    print(antenna_map)
    print(antenna_map.with_nodes())

    print(len(antenna_map.nodes))

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
        partA(Map.from_content(content))
    else:
        partB(Map.from_content(content))

if __name__ == "__main__":
    main()

