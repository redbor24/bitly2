## Description
The script returns the number of clicks on a Bitlink or Bitlink for a regular link.

## Requirements
    requests==2.26.0
    python-decouple==3.5

## How to install
    pip install -r requirements.txt

## Environment
The .env file must contain the token for the bitly.com API.

    BITLY_TOKEN = '<bitly.com_API_token>'

See [How to generate Bitly-token](https://app.bitly.com/settings/api/)

## Usage
    python main.py [url]

### Usage examples
    python main.py https://dvmn.org/encyclopedia/tutorial/tutorial_readme/
    Битлинк: https://bit.ly/3vxdSGu

    python main.py https://bit.ly/3vxdSGu
    Количество кликов: 0

    python main.py
    usage: main.py [url]
    
    The script returns the number of clicks on a Bitlink or Bitlink for a regular link.

    positional arguments:
      url  URL or Bitlink
