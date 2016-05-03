import cStringIO
import os
import sys
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
    
def read_file(text_path):
    with open(text_path, 'r') as f:
        read_data = f.read()
        return read_data
    
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
    print("----------------------\nPost request received")
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_tmp = cStringIO.StringIO(file.read())
        pil_image = Image.open(file_tmp)
    

        image_path = UPLOAD_FOLDER + "PIL_saved_image.jpg"
        print("Saving image to: " + image_path + "\n")
        
        pil_image.save(image_path)
        print("Image saved.\nProcessing text.\n")
        
        text_path = UPLOAD_FOLDER + "output.txt"
        text_path2 = UPLOAD_FOLDER + "output"
        eng.OCRProcessing(image_path, text_path2, nargout=0)
        text = read_file(text_path)
	print("OCR call")
	#text = ""
        #try:
        #    print(ocr)
        #    print(ocr.simple_ocr)
        #    text0 = ocr.simple_ocr(pil_image)
#	    text90 = ocr.simple_ocr(pil_image.rotate(90))
#	    text = text0 if len(text0) >= len(text90) else text90
#	    text180 = ocr.simple_ocr(pil_image.rotate(180))
#	    text = text180 if len(text180) > len(text) else text
#	    text270 = ocr.simple_ocr(pil_image.rotate(270))
	#    text270 = ocr.simple_ocr(pil_image.rotate(-90))
	#    text = text270 if len(text270) > len(text0) else text0
            
        #except:
        #    print("Unexpected error:", sys.exc_info()[0])
        print(text)
        return text
    return "Error"

if __name__ == "__main__":
    eng = matlab.engine.start_matlab()
    app.run(debug=True)
    eng.quit()

