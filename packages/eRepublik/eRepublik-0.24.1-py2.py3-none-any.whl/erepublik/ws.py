import websocket

try:
    import thread
except ImportError:
    import _thread as thread
import time


def on_message(ws, message):
    print(message)


def on_error(ws, error):
    print(error)


def on_close(ws):
    print("### closed ###")


def on_open(ws):
    def run(*args):
        for i in range(3):
            time.sleep(1)
            ws.send("AQAAMXsic3lzIjp7InR5cGUiOiJqcy13ZWJzb2NrZXQiLCJ2ZXJzaW9uIjoiMC4wLjEifX0=")
        time.sleep(1)
        ws.close()
        print("thread terminating...")

    thread.start_new_thread(run, ())


if __name__ == "__main__":
    ws = websocket.create_connection("wss://gate.erepublik.com:3050/")
    ws.send(b'\x01\x00\x001{"sys":{"type":"js-websocket","version":"0.0.1"}}')
    msg = ws.recv()
    print(1, msg)
    msg.decode('utf8')
    ws.send(b'\x04\x00\x000\x00\x01\x1bgate.gateHandler.queryEntry{"userId":1620414}')
    print(2, ws.recv())
    ws = websocket.create_connection("wss://battlefield2.erepublik.com:3050/")
    ws.send(b'{"sys":{"type":"js-websocket","version":"0.0.1"}}')
    while True:
        print(ws.recv())

    # websocket.enableTrace(True)
    # headers = {
    #     'Sec-WebSocket-Extensions': 'permessage-deflate; client_max_window_bits',
    #     'Sec-WebSocket-Key': "IMhDOmkK7HgnxKVefHAGAw==",
    #     "Sec-WebSocket-Version": "13",
    #     "Upgrade": "websocket"
    # }
    # ws = websocket.WebSocketApp("wss://gate.erepublik.com:3050", header=headers,
    #                             on_message=on_message,
    #                             on_error=on_error,
    #                             on_close=on_close)
    # ws.on_open = on_open
    # ws.run_forever()
