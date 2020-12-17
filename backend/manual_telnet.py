import argparse

from core import TelnetClient


def parse_args():
    parser = argparse.ArgumentParser(
        description='Test telnet manually')
    parser.add_argument('ip', help='ip')
    parser.add_argument('username', help='username')
    parser.add_argument('password', help='password')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = parse_args()
    telnet_client = TelnetClient(args.ip, args.username, args.password)

    finish = not telnet_client.login_host()
    while not finish:
        command = input('>').strip()
        if command == 'finish':
            telnet_client.logout_host()
            finish = True
        else:
            telnet_client.execute_command(command)
