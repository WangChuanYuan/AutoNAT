import argparse

from core import update_host

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Update IP of PC')
    parser.add_argument('ip', help='ip')
    parser.add_argument('mask', help='mask')
    parser.add_argument('--gateway', help='gateway')
    args = parser.parse_args()
    update_host(args.ip, args.mask, args.gateway)
