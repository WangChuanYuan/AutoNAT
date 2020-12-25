import asyncio
import websockets
import os

from backend.core import (update_host, TelnetClient)


async def run_test(websocket, path):
    # async for message in websocket:
    #     await websocket.send(message)

    # 默认测试所有的主机
    _ = await websocket.recv()

    # TODO: 保存旧地址

    # XYZ 内的主机 A
    update_host("10.0.0.11", "255.0.0.0", device="")
    # 测试 RTA 能够 PING 通所有的设备
    with TelnetClient("10.0.0.1", "", "CISCO") as client:
        for addr in ["10.0.0.1", "10.0.0.2", "10.0.0.11", "192.168.1.2", "192.168.1.1", "192.168.3.1", "192.168.3.2"]:
            await websocket.send(client.execute_command(f"ping {addr}"))
        await websocket.send(client.execute_command("ping 192.168.1.34"))
    # 测试 RTC
    with TelnetClient("10.0.0.2", "", "CISCO") as client:
        await websocket.send(client.execute_command("ping 192.168.1.35"))
    # 从主机 A 和 RTC PING 主机 B
    await websocket.send(os.popen("ping 192.168.3.2").read())
    with TelnetClient("10.0.0.2", "", "CISCO") as client:
        await websocket.send(client.execute_command("ping 192.168.3.2"))
    # 再次从主机 A 和 RTC PING 主机 B
    await websocket.send(os.popen("ping 192.168.3.2").read())
    with TelnetClient("10.0.0.2", "", "CISCO") as client:
        await websocket.send(client.execute_command("ping 192.168.3.2"))

    # XYZ 外的主机 B
    update_host("192.168.3.2", "255.255.255.0", "192.168.3.1", device="")
    await websocket.send(os.popen("curl 192.168.1.60").read())


if __name__ == "__main__":
    start_server = websockets.serve(run_test, "localhost", 8887)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
