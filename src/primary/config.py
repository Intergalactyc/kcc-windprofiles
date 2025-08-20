import configparser
import argparse


def _parse_cl():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="config.ini")
    args = parser.parse_args()
    return vars(args)


def _parse_cfg(filepath):
    config = configparser.ConfigParser()
    config.read(filepath)
    return {"datapath": config["paths"]["data"]}


def parse():
    args = _parse_cl()
    args.update(_parse_cfg(args["config"]))
    del args["config"]
    return args


if __name__ == "__main__":
    print(parse())
