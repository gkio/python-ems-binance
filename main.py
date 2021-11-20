import requests
import numpy as np
import talib
from calculate_asset import calculate_asset

ASSETS_URL = "https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true"
ASSET_CATEGORY = "BNB"
def filter_asset(asset):
    return asset['q'] == ASSET_CATEGORY

def getAssets():
    res = requests.get(ASSETS_URL)
    return list(filter(filter_asset, res.json()["data"]))

COUNT_CANDLES = 50
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

def calculate_ema(ema_20, ema_55, prev_ema_20, prev_ema_55):
    if ema_20 > ema_55 and prev_ema_20:
        if prev_ema_20 < prev_ema_55:
            # todo add logic to buy
            pass
    else:
        # todo add logic to sell
        pass

    return

def main():
    while True:
        assets = getAssets()
        print(len(assets))
        # todo remove [:1]
        for asset in assets[:1]:
            calculate_asset(asset)

if __name__ == '__main__':
    main()