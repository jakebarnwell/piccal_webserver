import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
#import cv2
from PIL import Image
from StringIO import StringIO
import numpy as np
import ocr

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['bmp', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def convert_to_cv(image_data):
    pil_image = Image.open(StringIO(image_data))
    cv2_image = np.array(pil_image)
    return cv2_image

@app.route("/", methods=['GET', 'POST'])
def index():
    return """
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="upload/" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    <p></p>
    """

@app.route("/upload/", methods=['POST'])
def uploads():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        pil_image = Image.open(StringIO(file.read()))
        text = ocr.simple_ocr(pil_image)
        #cv2_image = convert_to_cv(file.read())
        #extracted_texts, bboxes = ocr.extract_image_text(cv2_image)
        print(text)
        return text
    return "Error"

if __name__ == "__main__":
    app.run(debug=True)
