# website/coinbase_client.py
from decouple import config
from urllib.parse import urlencode


def generate_onramp_url(asset, amount_usd):
    base_url = "https://pay.coinbase.com/buy"

    params = {
        "appId": config("COINBASE_CDP_API_KEY_ID"),
        "asset": asset,
        "amount": amount_usd,
        "currency": "USD",
        "network": "sandbox",   # sandbox mode
    }

    return f"{base_url}?{urlencode(params)}"