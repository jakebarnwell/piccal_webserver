import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import cv2
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
    pil_image = Image.open(StringIO(image_data));
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
    <p>%s</p>
    """ % "<br>".join(os.listdir(app.config['UPLOAD_FOLDER'],))

@app.route("/upload/", methods=['POST'])
def uploads():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        cv2_image = convert_to_cv(file.read())
        extracted_texts, bboxes = ocr.extract_image_text(cv2_image)
        print(len(extracted_texts))
        print(extracted_texts)
        return str(extracted_texts)
    return "Error"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)