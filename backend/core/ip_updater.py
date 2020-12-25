# encoding: utf-8
import os
import logging
import platform


def _win_update_host(ip, mask, gateway=None, device="本地连接"):
    cmd = 'netsh interface ip set address name="' + device + '" source=static' + \
          ' addr=' + ip + \
          ' mask=' + mask
    if gateway:
        cmd += (' gateway=' + gateway)
    with os.popen(cmd, 'r') as p:
        res = p.read()
        print(res)
    return res


def _unix_update_host(ip, mask, gateway=None, device='eth0'):
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


def _mac_update_host(ip, mask, gateway=None, device='en0'):
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


def update_host(ip, mask, gateway=None):
    sysstr = platform.system()
    if sysstr == 'Windows':
        return _win_update_host(ip, mask, gateway, device="本地连接")
    elif sysstr == 'Linux':
        return _unix_update_host(ip, mask, gateway, device='eth0')
    elif sysstr == 'Darwin':
        return _mac_update_host(ip, mask, gateway, device='en0')
    else:
        logging.warning('Unsupported OS')
        return 'Unsupported OS'
