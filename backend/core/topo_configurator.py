import logging
from addict import Dict
import json

from .cmd_client import Commandline
from .telnet_client import TelnetClient


class TopoConfigurator(object):
    def __init__(self, config, ws=None):
        if isinstance(config, str):
            with open(config) as f:
                config = Dict(json.load(f))
        self.devices = {}
        self._prepare_devices(config)
        self.command_blocks = config.command_blocks
        self.ws = ws

    def _prepare_devices(self, config):
        self.devices[config.hostname] = [Commandline(), False]
        for d in config.devices:
            self.devices[d.hostname] = [TelnetClient(ip=d.ip, username='', password=d.password), False]

    def _close_devices(self):
        for d, _ in self.devices.values():
            d.logout_host()
        self.devices = {}

    def _get_device(self, hostname):
        device, login = self.devices[hostname]
        if not login:
            self.devices[hostname][1] = device.login_host()
        return device

    async def config(self):
        for block in self.command_blocks:
            device = self._get_device(block.device)
            for command in block.commands:
                output = device.execute_command(command)
                if self.ws:
                    await self.ws.send(json.dumps(
                    {
                        "device": block.device,
                        "command": command,
                        "output": output.strip(),
                    }
                ))
        self._close_devices()
