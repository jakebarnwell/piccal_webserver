import pytesseract
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
import re

def read_dictionary():
    english = set([])
    with open("/home/ubuntu/6s198-mit-fall-2016/project2/piccal_webserver/piccal/english.txt") as f:
        content = f.read().splitlines()
        for line in content:
            if "_" not in line:
                english.add(line.lower())
    print(len(english))
    return english

english = read_dictionary()

def clean_text(text):
    text = re.sub('[^0-9a-zA-Z,:-\p{P}]+', ' ', text)
    text = re.sub('[^;_];', ' ', text) 
    text = re.sub('\s+', ' ', text).strip()
    text = eliminate_non_words(text)
    text = re.sub('\b[^aiAI0-9]\b', ' ', text)
    text = re.sub('\s+', ' ', text).strip()
    return text

def simple_ocr(image):
    text = pytesseract.image_to_string(image)
    text = clean_text(text)
    return text

def eliminate_non_words(text):
    words = text.split(' ')
    new_words = []
    for word in words:
        to_lower = word.lower()
        if re.search("^[a-z][a-z]*$", to_lower) and to_lower not in english and not re.search("^[A-Z]", word):
            continue
        if len(to_lower) > 10 and to_lower not in english:
            continue
        new_words.append(word)
    text = " ".join(new_words)
    return text