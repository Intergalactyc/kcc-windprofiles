from windprofiles import Parser

parser = Parser(paths = ["data", "dem", "cid"])

def parse():
    return parser.parse()
