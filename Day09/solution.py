import sys


class MissingNode(Exception):
    pass

class Node:
    def __init__(self, value, *, id=None):
        self.id = id
        self.is_file = True if id is not None else False
        self.next = None
        self.prev = None
        self.value=value



    def set_next(self, node):
        next_node = self.next
        if next_node:
            next_node.prev = node
        self.next = node
        node.next = next_node
        node.prev = self
    
    def set_prev(self, node):
        prev_node = self.prev

        if prev_node:
            prev_node.next = node
        
        self.prev = node
        node.prev = prev_node
        node.next = self

    def __str__(self):
        if self.is_file:
            return f"[F{self.id}:{self.value}]"
        return f"[E:{self.value}]"

class LinkedList:
    def __init__(self):
        self.start = None
        self.end = None
        self.len = 0
    
    def add(self, value, id=None):
        n = Node(value, id=id)
        self.add_node(n)
        self.len += 1

    def add_node(self, node):
        if self.end:
            self.end.set_next(node)
            self.end = node
        else:
            self.start = self.end = node

    def iter(self):
        node = self.start
        while node:
            yield node
            node = node.next
    
    def iter_rev(self):
        node = self.end
        while node:
            yield node
            node = node.prev

    def __str__(self):
        return print_nodes(self.start)
    
def print_nodes(node):
    result = []
    while node:
        result.append(str(node))
        node = node.next

    return '->'.join(result) 


def generate_disk(nums):
    disk = []
    is_block = True
    block_id = 0
    for num in nums:
        content = None
        if is_block:
            content = block_id
            block_id += 1

        disk += [content] * num
        is_block = not is_block

    return disk

def partA(data):
    result = 0
    nums = list(map(int, data))
    disk = generate_disk(nums)
    # print(disk)

    start_i, stop_i = 0, len(disk)-1

    while start_i < stop_i:
        start, stop = disk[start_i], disk[stop_i]

        if start is None and not stop is None:
            disk[start_i] = stop
            disk[stop_i] = None
            start_i += 1

        if disk[stop_i] is None:
            stop_i -= 1

        if disk[start_i] is not None:
            start_i += 1
    
    for i, num in enumerate(disk):
        if num is None:
            break
        # print(i, num)
        result += i * num

    # print(filled)
    # print(disk)
    return result


def partB(data):
    result = 0
    nums = list(map(int, data))

    ll = LinkedList()

    file_index = 0
    for (i, num) in enumerate(nums):
        # print(i, num, end="")
        if i % 2 == 0:
            # print("file")
            ll.add(num, id=file_index)
            file_index += 1
            continue
        # print("empty")
        ll.add(num)
    # print(ll)

    for file_i, file_node in enumerate(ll.iter_rev()):
        if not file_node.is_file:
            continue
        # print()
        # print(f"Processing {file_node}")
        for empty_i, empty_node in enumerate(ll.iter()):
            if empty_node == file_node:
                # print("Reached file")
                break
            if empty_node.is_file:
                continue
            
            # print(f"Matching {empty_node} ", end="")
            if empty_node.value < file_node.value:
                # print(f"Space too small")
                continue

            # print(f"Match!")
            space_left = empty_node.value - file_node.value
            empty_a = Node(0)
            copied_file = Node(value=file_node.value, id=file_node.id)
            empty_b = Node(space_left)
            bind_nodes(empty_a, copied_file)
            bind_nodes(copied_file, empty_b)

            # print(f"Replacing {empty_node} with {print_nodes(empty_a)}")

            bind_nodes(empty_node.prev, empty_a)
            bind_nodes(empty_b, empty_node.next)

            # mark as empty
            file_node.is_file = False

            break
        # print(ll)
            

    print(ll)
    disk = []
    for node in ll.iter():
        if node.is_file:
            disk += [node.id] * node.value
        else:
            disk += [None] * node.value
    print(disk)
    for i, value in enumerate(disk):
        if value is None:
            continue
        result += i * value
    return result

def bind_nodes(node_a, node_b):
    node_a.next = node_b
    node_b.prev = node_a
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
        print(partA(content))
    else:
        print(partB(content))

if __name__ == "__main__":
    main()

