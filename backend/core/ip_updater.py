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
    res = os.system(cmd)
    if res == 0:
        print('修改成功')
    else:
        logging.warning('修改失败')


def _unix_update_host(ip, mask, gateway=None, device='eth0'):
    ip_cmd = 'ifconfig ' + device + ' ' + ip + ' netmask ' + mask
    res = os.system(ip_cmd)
    if res == 0:
        print('修改IP成功')
    else:
        logging.warning('修改IP失败')
        return
    if gateway:
        gw_cmd = 'route add default gw ' + gateway
        res = os.system(gw_cmd)
        if res == 0:
            print('修改网关成功')
        else:
            logging.warning('修改网关失败')


def _mac_update_host(ip, mask, gateway=None, device='en0'):
    ip_cmd = 'ifconfig ' + device + ' ' + ip + ' netmask ' + mask
    res = os.system(ip_cmd)
    if res == 0:
        print('修改IP成功')
    else:
        logging.warning('修改IP失败')
        return
    if gateway:
        gw_cmd = 'route add -net 0.0.0.0 ' + gateway
        res = os.system(gw_cmd)
        if res == 0:
            print('修改网关成功')
        else:
            logging.warning('修改网关失败')


def update_host(ip, mask, gateway=None):
    sysstr = platform.system()
    if sysstr == 'Windows':
        _win_update_host(ip, mask, gateway, device="本地连接")
    elif sysstr == 'Linux':
        _unix_update_host(ip, mask, gateway, device='eth0')
    elif sysstr == 'Darwin':
        _mac_update_host(ip, mask, gateway, device='en0')
    else:
        logging.warning('Unsupported OS')
