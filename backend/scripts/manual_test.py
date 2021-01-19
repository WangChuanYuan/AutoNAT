import os

from core import (update_host, TelnetClient)

LOCAL_INTERFACE = "enp0s20f0u4u4"


def main():
    # XYZ 内的主机 A
    update_host("10.0.0.11", "255.0.0.0", device=LOCAL_INTERFACE)

    # 测试 RTA 能够 PING 通所有的设备
    client = TelnetClient("10.0.0.1", "", "CISCO")
    client.login_host()
    for addr in ["10.0.0.1", "10.0.0.2", "10.0.0.11", "192.168.1.1", "192.168.1.2", "192.168.3.2", "192.168.3.4", "192.168.4.1"]:
        print(client.execute_command(f"ping {addr}"))
    print(client.execute_command("ping 192.168.1.34"))
    client.logout_host()

    # 测试 RTC
    client = TelnetClient("10.0.0.2", "", "CISCO")
    client.login_host()
    print(client.execute_command("ping 192.168.1.35"))
    client.logout_host()

    # 从主机 A 和 RTC PING 主机 B
    print(os.popen("ping -c 5 192.168.3.2").read())
    client = TelnetClient("10.0.0.2", "", "CISCO")
    client.login_host()
    print(client.execute_command("ping 192.168.3.2"))
    client.logout_host()

    # 再次从主机 A 和 RTC PING 主机 B
    print(os.popen("ping -c 5 192.168.3.2").read())
    client = TelnetClient("10.0.0.2", "", "CISCO")
    client.login_host()
    print(client.execute_command("ping 192.168.3.2"))
    client.logout_host()

    # # XYZ 外的主机 B
    # update_host("192.168.3.2", "255.255.255.0", "192.168.3.1", device=LOCAL_INTERFACE)
    # print(os.popen("curl 192.168.1.60").read())


if __name__ == "__main__":
    main()
