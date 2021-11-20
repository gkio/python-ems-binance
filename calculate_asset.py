import requests
import numpy as np
import talib

COUNT_CANDLES = 500
INTERVAL = "1m"

def get_asset_candles(ASSET):
    url = "https://www.binance.com/api/v3/klines?limit={}&symbol={}&interval={}".format(COUNT_CANDLES, ASSET, INTERVAL)
    res = requests.get(url)
    data = res.json()
    write_file = open("data.json", "w")
    write_file.write(str(data))
    write_file.close()
    return data

EMA_FROM=20
EMA_TO=55

def create_ema(asset_data):
    ema_from = talib.EMA(asset_data, EMA_FROM)
    ema_to = talib.EMA(asset_data, EMA_TO)

    return ema_from, ema_to


def fetch_and_normalize(asset):
    candles_data = get_asset_candles(asset)
    data = []
    for candle in candles_data:
        data.append(float(candle[4]))
    
    return np.array(data)

def get_ema(data):
    print(data)
    ema_from, ema_to = create_ema(data)
    return ema_from[-1], ema_to[-1]

def calculate_ema(asset, ema_from, ema_to, state):
    if ema_from > ema_to and state['prev_ema_from']:
        if state['prev_ema_from'] < state['prev_ema_to']:
            # todo add logic to buy
            print('buy '+ asset, state)
            pass
    else:
        print('sell '+ asset, state)
        # todo add logic to sell
        pass

    return

state = {
    'buy': False,
    'sell': True,
    'prev_ema_from': None,
    'prev_ema_to': None
}

def calculate_asset(asset):
    data = fetch_and_normalize(asset['s'])
    ema_from, ema_to = get_ema(data)
    calculate_ema(
        asset['s'],
        ema_from,
        ema_to,
        state,
    )
    state['prev_ema_from'] = ema_from
    state['prev_ema_to'] = ema_to
