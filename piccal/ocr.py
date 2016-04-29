import pytesseract
from PIL import Image
from PIL import ImageFilter
from StringIO import StringIO
from threading import Thread
import cv2
import re
import cv2

def read_dictionary():
    english = set([])
    with open("english.txt") as f:
        content = f.read().splitlines()
        for line in content:
            if "_" not in line:
                english.add(line.lower())
    print(len(english))
    return english

english = read_dictionary()

def process_image(url):
    image = _get_image(url)
    image.filter(ImageFilter.SHARPEN)
    print("hi")
    text = pytesseract.image_to_string(image)
    print(text)
    return text

def add_texts(detected_texts, extracted_texts):
    new_texts = []
    for extracted_text in extracted_texts:
        min_dist = float("inf")
        for text in detected_texts:
            dist = levenshtein(text, extracted_text)
            if dist < min_dist:
                min_dist = dist
        if min_dist > 2:
            detected_texts.append(extracted_text)
    return detected_texts

def eliminate_non_words(text):
    words = text.split(' ')
    new_words = []
    for word in words:
        to_lower = word.lower()
        if re.search("^[a-z][a-z]*$", to_lower) and to_lower not in english and not re.search("^[A-Z]", word):
            continue
        new_words.append(word)
    text = " ".join(new_words)
    return text
    
def clean_text(text):
    text = re.sub('[^0-9a-zA-Z,:-\p{P}]+', ' ', text)
    text = re.sub('\s+', ' ', text).strip()
    text = eliminate_non_words(text)
    text = eliminate_non_words(text)
    print(text)
    text = re.sub('\b[^aiAI0-9]\b', ' ', text)
    text = re.sub('\s+', ' ', text).strip()
    return text

def extract_subimage_text(rgb_img, bbox, index, extracted_texts):
    [x, y, w, h] = bbox
    sub_img = rgb_img[y:y+h, x:x+w]
    PIL_img = Image.fromarray(sub_img)
    extracted_text = clean_text(pytesseract.image_to_string(PIL_img))
    extracted_texts[index] = extracted_text
    
def extract_image_text(bgr_img):
    rgb_img = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2RGB)
    bboxes = find_text_bounds(bgr_img)
    
    extracted_texts = [None] * len(bboxes)
    
    threads = []
    for ind, bbox in enumerate(bboxes):
        t = Thread(target=extract_subimage_text, args=(rgb_img, bbox, ind, extracted_texts))
        t.start()
        threads.append(t)
    
    for thread in threads:
        thread.join()
    
    # Elminate empty results
    bboxes = [bbox for ind, bbox in enumerate(bboxes) if extracted_texts[ind] != ""]
    extracted_texts = [text for text in extracted_texts if text != ""]
    return extracted_texts, bboxes

def find_text_bounds(cv2_img):
    img2gray = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2gray, 180, 255, cv2.THRESH_BINARY)
    image_final = cv2.bitwise_and(img2gray , img2gray , mask =  mask)
    ret, new_img = cv2.threshold(image_final, 180 , 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV

    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3 , 3)) # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more 
    dilated = cv2.dilate(new_img, kernel, iterations = 9) # dilate , more the iteration more the dilation

    _, contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE) # get contours
    
    bboxes = []
    for contour in contours:
        # get rectangle bounding contour
        [x,y,w,h] = cv2.boundingRect(contour)

        #Don't plot small false positives that aren't text
        if w < 35 and h<35:
            continue
        bboxes.append([x, y, w, h])
    return bboxes
