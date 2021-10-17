import requests
from urllib import parse
from decouple import config


def shorten_link(token, long_url):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    if not parse.urlparse(long_url).scheme:
        _long_url = f'http://{long_url}'
    else:
        _long_url = long_url

    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json={"long_url": _long_url, "domain": "bit.ly"}
    )

    response.raise_for_status()
    return response.json()['link']


def count_clicks(token, bit_link):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        'unit': 'month',
        'units': '-1'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly/{parse.urlparse(bit_link).path}/clicks/summary',
        headers=headers,
        params=params
    )

    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(token, bit_link):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly/{parse.urlparse(bit_link).path}',
        headers=headers
    )

    return response.ok


if __name__ == '__main__':
    bitly_token = config('BITLY_TOKEN', '')
    url = input('Введите ссылку:')

    if is_bitlink(bitly_token, url):
        try:
            bitlink_click_count = count_clicks(bitly_token, url)
            print('Количество кликов', bitlink_click_count)
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка получения количества кликов по битлинку: {url}')
    else:
        try:
            bitlink = shorten_link(bitly_token, url)
            print('Битлинк', bitlink)
        except requests.RequestException as e:
            print(f'Ошибка формирования битлинка для {url}: {e}. Message: {e.response.json()["message"]}')
