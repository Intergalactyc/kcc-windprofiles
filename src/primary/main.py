from config import parse
from data import load_data


def main():
    args = parse()

    tower = load_data(args["datapath"])


if __name__ == "__main__":
    main()
