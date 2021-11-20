import requests
from calculate_asset import calculate_asset

ASSETS_URL = "https://www.binance.com/bapi/asset/v2/public/asset-service/product/get-products?includeEtf=true"
ASSET_CATEGORY = "BNB"

def filter_asset(asset):
    return asset['q'] == ASSET_CATEGORY

def getAssets():
    res = requests.get(ASSETS_URL)
    return list(filter(filter_asset, res.json()["data"]))

def main():
    while True:
        assets = getAssets()
        # todo remove [:1]
        for asset in assets[:1]:
            calculate_asset(asset)

if __name__ == '__main__':
    main()