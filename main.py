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
    response_json = response.json()
    try:
        response.raise_for_status()
    except requests.RequestException:
        if response_json['message'] == 'INVALID_ARG_LONG_URL':
            raise requests.RequestException(f'Некорректный URL - {long_url}')
        else:
            raise requests.RequestException(f'Ошибка - {response_json["message"]}')
    return response_json['link']


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
    response_data = response.json()

    try:
        response.raise_for_status()
    except requests.RequestException:
        if response_data['message'] == 'NOT_FOUND':
            raise requests.RequestException(f'некорректный URL - {response.url}')
        elif response_data['description'] == 'The value provided is invalid.':
            bad_param = response_data["errors"][0]["field"]
            raise requests.RequestException(f'некорректное значение параметра {bad_param} - {params}')
        else:
            raise requests.RequestException(response.json()['message'])
    return response_data['total_clicks']


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
        except requests.RequestException as e:
            print(f'Ошибка получения количества кликов по битлинку: {e}')
    else:
        try:
            bitlink = shorten_link(bitly_token, url)
            print('Битлинк', bitlink)
        except requests.RequestException as e:
            print(f'Ошибка формирования битлинка: {e}')
