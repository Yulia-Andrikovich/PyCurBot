import requests

import json


from config import keys

class APIExclusions(Exception):
    pass


class CurrencyConverter:
    @staticmethod
    def get_price(base: str, quote: str, amount: str):

        if quote == base:
            raise APIExclusions(f'You entered the same currency: {base}.')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIExclusions(f'Failed to process currency {base}')
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIExclusions(f'Failed to process currency {quote}')
        try:
            amount = float(amount)

        except ValueError:
            raise APIExclusions(f'It is not possible to process the amount of currency {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        content = json.loads(r.content)
        rate = content[keys[base]]

        return rate * amount


