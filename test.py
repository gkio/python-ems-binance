import websocket, json, pprint
import matplotlib.pyplot as plt
import numpy as np
import talib
from matplotlib.animation import FuncAnimation
import requests

COUNT_CANDLES = 500
INTERVAL = "1m"

ASSET = "ETHUSDT"
SOCKET = "wss://stream.binance.com:9443/ws/{}@kline_{}".format(ASSET.lower(), INTERVAL)

closes = []
in_position = False

def get_asset_candles(asset):
    url = "https://www.binance.com/api/v3/klines?limit={}&symbol={}&interval={}".format(COUNT_CANDLES, asset, INTERVAL)
    res = requests.get(url)
    data = res.json()
    return data

def fetch_and_normalize(asset):
    global closes
    candles_data = get_asset_candles(asset)
    data = []
    for candle in candles_data:
        data.append(float(candle[4]))
    
    closes = data

def on_message(ws, message):
    global closes, in_position
    
    json_message = json.loads(message)
    # pprint.pprint(json_message)

    candle = json_message['k']

    is_candle_closed = candle['x']
    close = candle['c']

    closes.append(float(close))
    if is_candle_closed:
        closes.append(float(close))
        closes_np = np.array(closes)
        ema_from = talib.EMA(closes_np, timeperiod=20)
        ema_to = talib.EMA(closes_np, timeperiod=55)
        
        print("EMA FROM AND TO")
        print(ema_from[-1], ema_to[-1])

def on_open(ws):
    print("openned connection")

def on_close(ws):
    print("closed connection")


def main():
    fetch_and_normalize(ASSET)
    ws = websocket.WebSocketApp(SOCKET, on_message=on_message, on_open=on_open, on_close=on_close)
    ws.run_forever()

if __name__ == '__main__':
    main()
