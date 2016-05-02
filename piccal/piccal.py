import cStringIO
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
#import cv2
from PIL import Image
from StringIO import StringIO
import numpy as np
import matlab.engine
import ocr

UPLOAD_FOLDER = '/tmp/'
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg'])

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
    log_file = open("/tmp/log.txt", "a")
    log_file.write("\n-----------------\nPost request received\n")
    log_file.write("Files:\n")
    log_file.write(str(request.files)+"\n")
    log_file.write("Headers:\n")
    log_file.write(str(request.files['file'].headers)+"\n")

    file = request.files['file']
    if file and allowed_file(file.filename):
        log_file.write("Processing File...\n")

        filename = secure_filename(file.filename)
        log_file.write("Filename is: " + str(filename) + "\n")
        
	pil_image = Image.open(cStringIO.StringIO(file.read()))

	image_save_path = "/tmp/temp_image.jpg"
        pil_image.save(image_save_path)
        log_file.write("Image saved to: " + image_save_path + "\n")
        text = ocr.simple_ocr(pil_image)

        text_file = open("/tmp/ocr.txt", "w")
        text_file.write(text)
	text_file.close()
#        eng = matlab.engine.start_matlab()
#        eng.OCRProcessing(image_save_path, "/tmp/ocr.txt")
        #cv2_image = convert_to_cv(file.read())
        #extracted_texts, bboxes = ocr.extract_image_text(cv2_image)
#        print(text)
        log_file.write("OCR:\n" + text + "\n")
        log_file.close()
        return text
    return "Error"

if __name__ == "__main__":
    app.run(debug=True)

