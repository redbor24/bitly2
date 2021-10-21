## Description
The script returns the number of clicks on a Bitlink or Bitlink for a regular link.

## Requirements
    requests==2.26.0
    python-decouple==3.5

## Usage
    $ python main.py [url]

## Usage examples
    $ python main.py https://dvmn.org/encyclopedia/tutorial/tutorial_readme/
    Битлинк: https://bit.ly/3vxdSGu

    $ python main.py https://bit.ly/3vxdSGu
    Количество кликов: 0

    $ python main.py
    usage: main.py [url]
    
    The script returns the number of clicks on a Bitlink or Bitlink for a regular link

    positional arguments:
      url  URL or Bitlink
