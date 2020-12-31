#!/usr/bin/env python

import asyncio
import io
import json
import logging
import websockets
import os

from core import (update_host, TelnetClient)

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")


async def run_tests(ws, path):
    # await ws.send("hahaha")

    message = await ws.recv()
    logging.info(f"path: {path}, message: '{message}'")
    if message != "test_NAT":
        await ws.send("error: invalid request")
        return

    with io.open("backend/resources/nat_test.json") as f:
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
                            # "success": "0% packet loss" in output,
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
                            # "success": "Success rate is 100 percent" in output,
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
                        # "success": "200 OK" in output,
                        "output": output.strip(),
                    }
                ))
            else:
                raise ValueError(f"unsupported command: '{tokens[0]}'")
    await ws.send(json.dumps({"result": success}))
    logging.info("test done")

# # XYZ 内的主机 A
# update_host("10.0.0.11", "255.0.0.0", device="")
# # 测试 RTA 能够 PING 通所有的设备
# with TelnetClient("10.0.0.1", "", "CISCO") as client:
#     for addr in ["10.0.0.1", "10.0.0.2", "10.0.0.11", "192.168.1.2", "192.168.1.1", "192.168.3.1", "192.168.3.2"]:
#         await websocket.send(client.execute_command(f"ping {addr}"))
#     await websocket.send(client.execute_command("ping 192.168.1.34"))
#
# # 测试 RTC
# with TelnetClient("10.0.0.2", "", "CISCO") as client:
#     await websocket.send(client.execute_command("ping 192.168.1.35"))
#
# # 从主机 A 和 RTC PING 主机 B
# await websocket.send(os.popen("ping 192.168.3.2").read())
#
# with TelnetClient("10.0.0.2", "", "CISCO") as client:
#     await websocket.send(client.execute_command("ping 192.168.3.2"))
#
# # 再次从主机 A 和 RTC PING 主机 B
# await websocket.send(os.popen("ping 192.168.3.2").read())
#
# with TelnetClient("10.0.0.2", "", "CISCO") as client:
#     await websocket.send(client.execute_command("ping 192.168.3.2"))
#
# # XYZ 外的主机 B
# update_host("192.168.3.2", "255.255.255.0", "192.168.3.1", device="")
# await websocket.send(os.popen("curl 192.168.1.60").read())

if __name__ == "__main__":
    start_server = websockets.serve(run_tests, "localhost", 8887)

    logging.info("auto test server started")

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
