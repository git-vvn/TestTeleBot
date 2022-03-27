import requests
import json
from cfg import keys, API_KEY

class APIException(Exception):
    pass

class Currencyconverter():
    @staticmethod
    def get_price(target: str, src: str, quantity: str):
        symbols_arr = []
        if target == src:
            raise APIException('Невозможно перевести одинаковые валюты!')

        try:
            src_ticker = keys[src]
        except KeyError:
            raise APIException(f'Ошибка в написании валюты {src}')

        try:
            target_ticker = keys[target]
        except KeyError:
            raise APIException(f'Ошибка в написании валюты {target}')

        try:
            quantity = float(quantity)
        except ValueError:
            raise APIException(f'Ошибка определения количества ({quantity}) переводимой валюты!')
        #########################
        ## +- Динамическое изменение массива валют
        for elem in keys.values():
            symbols_arr.append(elem)
        symbols_str = ",".join(map(str, symbols_arr))
        result = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key={API_KEY}&symbols={symbols_str}')
        #### Закомментированный вызов - платный, также как и изменение base-валюты API
        # exchangeEndpoint = f'http://api.exchangeratesapi.io/v1/convert?access_key='{API_KEY}'&from='{src_ticker}'&to='{target_ticker}'&amount='{keys[quantity]}
        ### Лекарство от жадности - пересчитываем курсы на основе бесплатных данных
        courses = json.loads(result.content)['rates']
        total_price = courses[src_ticker] / courses[target_ticker] * float(quantity)
        return total_price
