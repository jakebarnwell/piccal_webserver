import pytesseract
import requests
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO


def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    print("hi")
    text = pytesseract.image_to_string(image)
    print(text)
    return text


def _get_image(url):
    return Image.open(StringIO(requests.get(url).content))
