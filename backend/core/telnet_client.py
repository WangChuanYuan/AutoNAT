# encoding: utf-8

import logging
import telnetlib
import time


class TelnetClient(object):
    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.tn = telnetlib.Telnet()

    def login_host(self) -> bool:
        try:
            self.tn.open(self.ip, port=23)
        except:
            logging.error(f'{self.ip} 网络连接失败')
            return False
        # 等待login出现后输入用户名，最多等待10秒
        self.tn.read_until(b'login: ', timeout=10)
        self.tn.write(self.username.encode('ascii') + b'\n')
        # 等待Password出现后输入用户名，最多等待10秒
        self.tn.read_until(b'Password: ', timeout=10)
        self.tn.write(self.password.encode('ascii') + b'\n')
        # 延时两秒再收取返回结果，给服务端足够响应时间
        time.sleep(2)
        # 获取登录结果
        # read_very_eager()获取到的是的是上次获取之后本次获取之前的所有输出
        command_result = self.tn.read_very_eager().decode('ascii')
        if 'Login incorrect' not in command_result:
            print('%s登录成功' % self.ip)
            return True
        else:
            logging.error(f'{self.ip} 登录失败，用户名或密码错误')
            return False

    def logout_host(self):
        self.tn.write(b'exit\n')

    def execute_command(self, command) -> str:
        # 执行命令
        self.tn.write(command.encode('ascii') + b'\n')
        time.sleep(2)
        return self.tn.read_very_eager().decode('ascii')

    def __enter__(self):
        return self if self.login_host() else None

    def __exit__(self, typ, val, traceback):
        self.logout_host()
