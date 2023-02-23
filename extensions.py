import requests
import json
from config import keys, crypto, ROUND_CRYPTO


class APIException(Exception):
    pass


class ConverterClass:
    @staticmethod
    def get_price(quote: str, base: str, amount: str):
        try:
            quote_ticker = keys[quote]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{quote}"')

        try:
            base_ticker = keys[base]
        except KeyError:
            raise APIException(f'Не удалось обработать валюту "{base}"')

        try:
            amount = amount.replace(',', '.')
            amount = float(amount)
        except ValueError:
            raise APIException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
        if base in crypto:
            total_base = round(json.loads(r.content)[keys[base]] * amount, ROUND_CRYPTO)
        else:
            total_base = round(json.loads(r.content)[keys[base]] * amount, 2)

        if total_base < 0.0001:  # чтобы избавиться от экспоненты
            return 'менее 0.0001\nУкажите большее количество валюты для точного расчёта'
        else:
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

        if quote == 'рубль' or quote == 'юань':
            if int(int(amount)) % 10 != 1 or int(int(amount)) == 11:
                quote = quote[:-1] + 'ей'
            else:
                quote = quote[:-1] + 'я'

        return quote

    @staticmethod
    def base_end(base: str, amount: str):
        if base == 'доллар':
            base += 'ах'

        if base == 'рубль' or base == 'юань':
            base = base[:-1] + 'ях'

        if base in crypto:
            base += 'е'

        return base


def input_values(message):
    values = message.text.split(' ')
    if len(values) > 3:
        raise APIException('Слишком много параметров')
    elif len(values) == 2:  # для удобства юзера можно не указывать количество
        values.append('1')  # в таком случае количество принимается за 1
    elif len(values) < 2:
        raise APIException('Слишком мало параметров')
    values = list(map(str.lower, values))
    return values
