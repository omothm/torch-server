"""Torch Server test
"""

__author__ = "Omar Othman <omar@omothm.com>"


import os
import json
import requests
import urllib.parse

_CURRENT_DIR = os.path.dirname(__file__)
_URL = "http://localhost:8000/api/"


def main():
    """Sends a GET request to the server and prints the response
    """

    # get an example base-64 encoded image from an input file
    with open(os.path.join(_CURRENT_DIR, "input\\base64_example.txt")) as b64file:
        example_base64 = b64file.read()

    # send a GET request to the server
    res = requests.get(url=_URL, params={"service": "banknote","image":urllib.parse.quote_plus(example_base64)})

    print(res.text)


if __name__ == "__main__":
    main()
