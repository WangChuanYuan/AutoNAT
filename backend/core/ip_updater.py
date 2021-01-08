# encoding: utf-8

import os
import logging
import platform


def update_host(ip, mask, gateway=None, device=None) -> str:
    _lookup_table = {
        'Windows': _win_update_host,
        'Linux': _unix_update_host,
        'Darwin': _mac_update_host,
    }
    try:
        return _lookup_table[platform.system()](ip, mask, gateway=gateway, device=device)
    except KeyError:
        logging.warning('Unsupported OS')
        return 'Unsupported OS'


def _win_update_host(ip, mask, gateway=None, device=None):
    if device is None:
        device = '本地连接'

    cmd = f'netsh interface ip set address name="{device}" source=static addr={ip} mask={mask}'
    if gateway:
        cmd += (' gateway=' + gateway)
    with os.popen(cmd, 'r') as p:
        res = p.read()
        print(res)
    return res


def _unix_update_host(ip, mask, gateway=None, device=None):
    if device is None:
        device = 'enp0s20f0u1u4'

    ip_cmd = 'ifconfig ' + device + ' ' + ip + ' netmask ' + mask
    res = ''
    with os.popen(ip_cmd, 'r') as p:
        ip_res = p.read()
        res += ip_res
        print(ip_res)
    if gateway:
        gw_cmd = 'route add default gw ' + gateway
        with os.popen(gw_cmd, 'r') as p:
            gw_res = p.read()
            res += gw_res
            print(gw_res)
    return res


def _mac_update_host(ip, mask, gateway=None, device=None):
    if device is None:
        device = 'en0'

    ip_cmd = 'ifconfig ' + device + ' ' + ip + ' netmask ' + mask
    res = ''
    with os.popen(ip_cmd, 'r') as p:
        ip_res = p.read()
        res += ip_res
        print(ip_res)
    if gateway:
        gw_cmd = 'route add -net 0.0.0.0 ' + gateway
        with os.popen(gw_cmd, 'r') as p:
            gw_res = p.read()
            res += gw_res
            print(gw_res)
    return res
