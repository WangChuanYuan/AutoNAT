# encoding: utf-8

import os
import logging
import platform


def update_host(ip, mask, gateway=None, device=None):
    _lookup_table = {
        "Windows": _win_update_host,
        "Linux": _unix_update_host,
        "Darwin": _mac_update_host,
    }
    try:
        _lookup_table[platform.system()](ip, mask, gateway=gateway, device=device)
    except KeyError:
        logging.warning('Unsupported OS')


def _win_update_host(ip, mask, gateway=None, device=None):
    if device is None:
        device = "本地连接"

    cmd = f'netsh interface ip set address name="{device}" source=static addr={ip} mask={mask}'
    if gateway:
        cmd += f' gateway={gateway}'
    if os.system(cmd) == 0:
        logging.info('修改 IP 成功')
        logging.info('修改网关成功')
    else:
        logging.error('修改 IP 失败')
        logging.error('修改网关失败')


def _unix_update_host(ip, mask, gateway=None, device=None):
    if device is None:
        device = "eth0"

    ip_cmd = f"ifconfig {device} {ip} netmask {mask}"
    if os.system(ip_cmd) == 0:
        logging.info('修改 IP 成功')
        if gateway:
            gw_cmd = f'route add default gw {gateway}'
            if os.system(gw_cmd) == 0:
                logging.info('修改网关成功')
            else:
                logging.error('修改网关失败')
    else:
        logging.error('修改 IP 失败')


def _mac_update_host(ip, mask, gateway=None, device=None):
    if device is None:
        device = "en0"

    ip_cmd = f"ifconfig {device} {ip} netmask {mask}"
    if os.system(ip_cmd) == 0:
        logging.info('修改 IP 成功')
        if gateway:
            gw_cmd = f'route add -net 0.0.0.0 {gateway}'
            if os.system(gw_cmd) == 0:
                logging.info('修改网关成功')
            else:
                logging.error('修改网关失败')
    else:
        logging.error('修改 IP 失败')
