# encoding: utf-8
import time
import subprocess

from .device import Device
from .ip_updater import update_host


class Commandline(Device):

    def login_host(self):
        return True

    def logout_host(self):
        pass

    def execute_command(self, command):
        command = command.strip()
        if not command:
            return ''
        args = command.split(' ')
        if args[0] == 'update':
            assert len(args) == 3 or len(args) == 4
            args = tuple(args[1:])
            return update_host(*args)
        else:
            p = subprocess.Popen(command, stderr=subprocess.STDOUT, stdout=subprocess.PIPE, shell=True)
            t_beginning = time.time()
            while True:
                if p.poll() is not None:
                    break
                seconds_passed = time.time() - t_beginning
                if seconds_passed > 5:
                    p.terminate()
                time.sleep(0.1)
            res = p.stdout.read().decode('ascii')
            print(res)
            return res
