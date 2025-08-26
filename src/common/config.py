from windprofiles import Parser

parser = Parser(paths = ["data", "dem"])

def parse():
    return parser.parse()

if __name__ == "__main__":
    print(parse())
