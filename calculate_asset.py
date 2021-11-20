import requests
import numpy as np
import talib

COUNT_CANDLES = 100
INTERVAL = "5m"

def get_asset_candles(ASSET):
    url = "https://www.binance.com/api/v3/klines?limit={}&symbol={}&interval={}".format(COUNT_CANDLES, ASSET, INTERVAL)
    res = requests.get(url)
    return res.json()

def create_ema(assetData):
    ema_20 = talib.EMA(assetData, 20)
    ema_55 = talib.EMA(assetData, 55)

    return ema_20, ema_55


def fetch_and_normalize(asset):
    candles_data = get_asset_candles(asset)
    data = []
    for candle in candles_data:
        data.append(float(candle[4]))
    
    return np.array(data)

def get_ema(data):
    ema_20, ema_55 = create_ema(data)
    return ema_20[-1], ema_55[-1]

def calculate_ema(ema_20, ema_55, state):
    if ema_20 > ema_55 and state['prev_ema_20']:
        if state['prev_ema_20'] < state['prev_ema_55']:
            # todo add logic to buy
            pass
    else:
        print(state['prev_ema_20'])
        # todo add logic to sell
        pass

    return

state = {
    'buy': False,
    'sell': True,
    'prev_ema_20': None,
    'prev_ema_55': None
}

def calculate_asset(asset):
    data = fetch_and_normalize(asset['s'])
    ema_20, ema_55 = get_ema(data)
    calculate_ema(
        ema_20,
        ema_55,
        state,
    )
    state['prev_ema_20'] = ema_20
    state['prev_ema_55'] = ema_55
