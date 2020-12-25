import argparse

from core import TopoConfigurator


def parse_args():
    parser = argparse.ArgumentParser(
        description='Config NAT automatically')
    parser.add_argument('config', help='path of config file')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    configurator = TopoConfigurator(args.config)
    configurator.config()
