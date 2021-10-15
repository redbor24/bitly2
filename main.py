import requests
from urllib import parse
from decouple import config


def shorten_link(token, url):
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json',
    }

    if not parse.urlparse(url).scheme:
        _url = f'http://{url}'
    else:
        _url = url

    response = requests.post(
        'https://api-ssl.bitly.com/v4/shorten',
        headers=headers,
        json={"long_url": _url, "domain": "bit.ly"}
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.json()['message'] == 'INVALID_ARG_LONG_URL':
            raise requests.exceptions.HTTPError(f'Некорректный URL - {url}')
        else:
            raise requests.exceptions.HTTPError(f'Ошибка - {response.json()["message"]}')
    return response.json()['link']


def count_clicks(token, bit_link):
    headers = {
        'Authorization': f'Bearer {token}'
    }

    params = {
        ('unit', 'month'),
        ('units', '-1')
    }

    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/bit.ly/{parse.urlparse(bit_link).path}/clicks/summary',
        headers=headers,
        params=params
    )

    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError:
        if response.json()['message'] == 'NOT_FOUND':
            raise requests.exceptions.HTTPError(f'некорректный URL - {response.url}')
        elif response.json()['description'] == 'The value provided is invalid.':
            bad_param = response.json()["errors"][0]["field"]
            raise requests.exceptions.HTTPError(f'некорректное значение параметра {bad_param} - {params}')
        else:
            raise requests.exceptions.HTTPError(response.json()['message'])
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
    link = input('Введите ссылку:')

    if is_bitlink(bitly_token, link):
        try:
            cnt = count_clicks(bitly_token, link)
            print('Количество кликов', cnt)
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка получения количества кликов по битлинку: {e}')
    else:
        try:
            bitlink = shorten_link(bitly_token, link)
            print('Битлинк', bitlink)
        except requests.exceptions.HTTPError as e:
            print(f'Ошибка формирования битлинка: {e}')
