import argparse

from core import update_host


def parse_args():
    parser = argparse.ArgumentParser(
        description='Update IP of PC')
    parser.add_argument('ip', help='ip')
    parser.add_argument('mask', help='mask')
    parser.add_argument('--gw', help='gateway')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    update_host(args.ip, args.mask, args.gw)
