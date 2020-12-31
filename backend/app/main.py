#!/usr/bin/env python

import asyncio
import os
import websockets

from flask import Flask, jsonify

import backend.auto_test_nat

app = Flask(__name__)


@app.route('/test', methods=['GET'])
def test_NAT():
    url = 'ws://localhost:8887'
    with websockets.connect(url) as ws:
        ws.send('test_NAT')
        return jsonify(ws.recv())


@app.route('/config', methods=['GET', 'POST'])
def config_NAT(args):
    return None


if __name__ == '__main__':
    app.run()
