import os
import sys
from flask import Flask, request, redirect, url_for
#import cv2
from PIL import Image
from StringIO import StringIO
import numpy as np
import matlab.engine
import ocr
import time
import image_processing

UPLOAD_FOLDER = '/home/ubuntu/tmp_images/'
ALLOWED_EXTENSIONS = set(['bmp', 'png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
use_matlab = True

if use_matlab:
    #eng = matlab.engine.start_matlab('-nodisplay -nosplash -nojvm -nodesktop')
    eng = matlab.engine.connect_matlab()
    print("Sqrt(4) is: " + str(eng.sqrt(4.0)))
    print("MATLAB engine obtained.")

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
    
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
    
    ## Process form data
    if 'orientation' in request.form:
        orientation = int(request.form.get('orientation'))
    else:
        orientation = 0
        
    if 'corners' in request.form:
        corners = request.form.get('corners')
        print("Corners detected in form request")
    else:
        corners = "0.0 0.0 1.0 0.0 1.0 1.0 0.0 1.0"    
    corners = [float(coordinate) for coordinate in corners.split(" ")]
    
    print("Corners: " + str(corners))
    print("Orientation is: " + str(orientation))
    
    if file and allowed_file(file.filename):
        uploaded_image = image_processing.OCRImage(file, orientation)
        uploaded_image.save(UPLOAD_FOLDER)

        text = ""
        
        print("here_1")
        if use_matlab:
            print("here_2")
            text = uploaded_image.matlab_ocr(eng, UPLOAD_FOLDER, corners)
        
        if (len(text) < 3) or not use_matlab:
            print("Using simple ocr")
            text = uploaded_image.simple_ocr()
            
        print("All OCR complete. Cleaned OCR text:\n ")
        print(text)
        return text
    return "Error"

if __name__ == "__main__":
    app.run(debug=True)

