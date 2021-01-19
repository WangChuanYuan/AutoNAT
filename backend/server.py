#!/usr/bin/env python

import asyncio
import argparse
import io
import json
import logging
import websocketss
import os

from core import (update_host, TelnetClient, TopoConfigurator)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


config_file = "resources/static_nat_config.json"
test_file = "resources/nat_test.json"

async def run(ws, path):
    while True:
        message = await ws.recv()
        logging.info(f"path: {path}, message: '{message}'")
        if message not in ["config_NAT", "test_NAT"]:
            await ws.send("error: invalid request")
            continue

        if message == "config_NAT":
            configurator = TopoConfigurator(config_file, ws)
            await configurator.config()
            await ws.send(json.dumps({"result": "配置完成"}))
            continue

        with io.open(test_file) as f:
            obj = json.load(f)
            devices = {dev["name"]: dev for dev in obj["devices"]}
            testcases = obj["testcases"]
            local_interface = obj["local_interface"]

        success = True
        for tc in testcases:
            for cmd in tc["before"]:
                tokens = cmd.split()
                if tokens[0] == "as":
                    dev = devices[tokens[1]]
                    ip, mask, gateway = dev["addr"], dev["mask"], dev["gateway"]
                    update_host(ip, mask, gateway=gateway, device=local_interface)
                else:
                    raise ValueError(f"unsupported command: '{tokens[0]}'")

            client: TelnetClient = None
            curr_device = "local"
            for cmd in tc["commands"]:
                tokens = cmd.split()
                if tokens[0] == "login":
                    dev = devices[tokens[1]]
                    client = TelnetClient(dev["addr"], "", dev["password"])
                    client.login_host()
                    curr_device = tokens[1]
                elif tokens[0] == "logout":
                    client.logout_host()
                    client = None
                    curr_device = "local"
                elif tokens[0] == "ping":
                    if client is None:
                        # PING from local
                        output = os.popen(f"ping -c 5 {tokens[1]}").read()
                        success = "0% packet loss" in output
                        await ws.send(json.dumps(
                            {
                                "device": curr_device,
                                "command": cmd,
                                "output": output.strip(),
                            }
                        ))
                    else:
                        output = client.execute_command(cmd)
                        success = "Success rate is 100 percent" in output
                        await ws.send(json.dumps(
                            {
                                "device": curr_device,
                                "command": cmd,
                                "output": output.strip(),
                            }
                        ))
                elif tokens[0] == "curl":
                    # -I means "header only"
                    output = os.popen(f"curl -I {tokens[1]}").read()
                    success = "200 OK" in output
                    await ws.send(json.dumps(
                        {
                            "device": curr_device,
                            "command": cmd,
                            "output": output.strip(),
                        }
                    ))
                else:
                    raise ValueError(f"unsupported command: '{tokens[0]}'")
        await ws.send(json.dumps({"result": "测试成功" if success else "测试失败"}))
        logging.info("test done")


def parse_args():
    parser = argparse.ArgumentParser(
        description='Run WebSockets server')
    parser.add_argument('--config', help='path of config file')
    parser.add_argument('--test', help='path of test file')
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = parse_args()
    if args.config:
        config_file = args.config
    if args.test:
        test_file = args.test

    start_server = websockets.serve(run, "localhost", 8887)

    logging.info("auto test server started")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
