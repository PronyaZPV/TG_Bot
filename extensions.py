import requests
import json
from config import keys


class APIException(Exception):
    pass


class ConverterClass:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {quote}')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту {base}')

        try:
            amount = amount.replace(',', '.')
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество {amount}')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        total_base = round(json.loads(r.content)[keys[base]] * amount, 2)

        return total_base


class Ending:
    @staticmethod
    def quote_end(quote: str, amount: str):
        amount = amount.split('.')[0]
        amount = amount.split(',')[0]
        if quote == 'доллар' or quote == 'биткоин' or quote == 'эфириум':
            if int(int(amount)) % 10 != 1 or int(int(amount)) == 11:
                quote += 'ов'
            else:
                quote += 'a'

        if quote == 'рубль':
            if int(int(amount)) % 10 != 1 or int(int(amount)) == 11:
                quote = quote[:-1] + 'ей'
            else:
                quote = quote[:-1] + 'я'

        return quote

    @staticmethod
    def base_end(base: str, amount: str):
        if base == 'доллар':
            base += 'ах'

        if base == 'рубль':
            base = base[:-1] + 'ях'

        return base
