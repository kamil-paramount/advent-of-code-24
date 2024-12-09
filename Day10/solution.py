import sys


def partA(data):
    result = 0
    return result

def partB(data):
    result = 0
    return result

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

