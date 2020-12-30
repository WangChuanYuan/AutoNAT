from flask import Flask, jsonify
import server
import asyncio
import websockets
import os

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
