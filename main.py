import requests
import json
from urllib import parse
from decouple import config


def shorten_link(token, url):
    if not token:
        raise Exception('Ошибка! Токен не задан!')

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    if not parse.urlparse(url).scheme:
        fu = parse.urlparse(link)._replace(scheme='http://')
        url = f'{fu.scheme}{fu.netloc}{fu.path}{fu.params}{fu.query}{fu.fragment}'

    json_str = json.dumps({"long_url": url, "domain": "bit.ly"})
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, data=json_str)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.json()['message'] == 'INVALID_ARG_LONG_URL':
            raise Exception(f'некорректный URL - {url}')
    return response.json()['link']


def count_clicks(token, bitlink):
    if not token:
        raise Exception('Ошибка! Токен не задан!')

    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        ('unit', 'month'),
        ('units', '-1')
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly/{parse.urlparse(bitlink).path}/clicks/summary',
        headers=headers, params=params
    )
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        if response.json()['message'] == 'NOT_FOUND':
            raise Exception(f'некорректный URL - {response.url}')
        elif response.json()['description'] == 'The value provided is invalid.':
            bad_param = response.json()["errors"][0]["field"]
            raise Exception(f'некорректное значение параметра {bad_param} - {params}')
        else:
            raise err
    return response.json()['total_clicks']


def is_bitlink(token, link):
    if not token:
        raise Exception('Ошибка! Токен не задан!')

    headers = {
        'Authorization': f'Bearer {token}'
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly/{parse.urlparse(link).path}',
        headers=headers
    )
    return response.ok


if __name__ == '__main__':
    my_token = config('token', '')
    link = input('Введите ссылку:')

    if is_bitlink(my_token, link):
        try:
            cnt = count_clicks(my_token, link)
            print('Количество кликов', cnt)
        except Exception as e:
            print(f'Ошибка получения количества кликов по битлинку: {e}')
    else:
        try:
            bitlink = shorten_link(my_token, link)
            print('Битлинк', bitlink)
        except Exception as e:
            print(f'Ошибка формирования битлинка: {e}')
