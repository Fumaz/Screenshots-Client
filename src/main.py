import os
import random
import string
import sys
from io import BytesIO

import pyperclip
import requests
from PIL import Image

import config


def random_filename() -> str:
    return ''.join(random.choices(string.ascii_letters, k=5)) + '.png'


def get_png() -> str:
    filename = random_filename()

    sys.stdin = os.fdopen(sys.stdin.fileno(), 'rb', 0)
    data = bytearray(sys.stdin.read())

    image = Image.open(BytesIO(data))
    image.save(filename)

    return filename


def main():
    image = get_png()

    url = f'https://{config.DOMAIN}/upload'
    files = {'image': (image, open(image, 'rb'), 'image/png')}
    data = {'api_key': config.API_KEY}

    request = requests.post(url, data=data, files=files)

    os.remove(image)

    pyperclip.copy(request.json()['url'])


if __name__ == '__main__':
    main()
