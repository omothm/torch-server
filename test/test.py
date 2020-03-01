"""Torch Server test
"""

__author__ = "Omar Othman <omar@omothm.com>"


import os
import json
import requests


_CURRENT_DIR = os.path.dirname(__file__)
_URL = "http://localhost:8000/api/"


def main():
    """Sends a GET request to the server and prints the response
    """

    # get a url-safe base-64 image encoding from an input file
    with open(os.path.join(_CURRENT_DIR, "input\\url_safe.txt")) as b64file:
        urlsafe_base64 = b64file.read()

    # build the request
    request = {
        "request": "banknote",
        "image": urlsafe_base64
    }
    request_str = json.dumps(request)

    # send a GET request to the server
    res = requests.get(url=_URL, params={"query": request_str})

    print(res.text)


if __name__ == "__main__":
    main()
