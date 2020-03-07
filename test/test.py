"""Torch Server test

Sends GET and POST requests to the server.
"""

__author__ = "Omar Othman <omar@omothm.com>"


import os
import urllib.parse
import requests


_CURRENT_DIR = os.path.dirname(__file__)
_URL = "http://localhost:8000/api/"


def main():
    """Sends GET and POST requests to the server and prints the response
    """

    # get an example base-64 encoded image from an input file
    with open(os.path.join(_CURRENT_DIR, "input", "base64_example.txt")) as b64file:
        example_base64 = b64file.read()

    service = "banknote"

    print("Sending a GET request...")
    res = requests.get(url=_URL, params={
        "service": service,
        "image": urllib.parse.quote_plus(example_base64)
    })
    print(res.text)

    print()
    print("Sending a POST request...")
    url = f"{_URL}?service={service}"
    res = requests.post(url=url, data=example_base64)
    print(res.text)


if __name__ == "__main__":
    main()
