import requests
from typing import Union

bitcoin_url = "https://api.coindesk.com/v1/bpi/currentprice/USD.json"


def get_btc_price() -> Union[None, str]:
    """Функция для получения цены биткоина в долларах в строковом формате"""
    response = requests.get(bitcoin_url)
    data = response.json()
    return data["bpi"]["USD"]["rate"]
