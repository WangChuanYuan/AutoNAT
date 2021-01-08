#!/usr/bin/env bash

#
# 准备环境
#

sudo ifconfig wlp2s0 down
sudo python backend/update_ip.py 10.0.0.11 255.0.0.0 --gateway 10.0.0.1
