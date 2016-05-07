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
import time

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
    
    ## Process form data
    if 'orientation' in request.form:
        orientation = int(request.form.get('orientation'))
    else:
        orientation = 0
        
    if 'corners' in request.form:
        corners = request.form.get('corners')
        print("Corners detected in form request")
    else:
        corners = "0.0 0.0 0.0 1.0 1.0 0.0 1.0 1.0"    
    corners = [float(coordinate) for coordinate in corners.split(" ")]
    corners = [(corners[0], corners[1]), (corners[2], corners[3]), (corners[4], corners[5]), (corners[6], corners[7])]
    
    print("Corners: " + str(corners))
    print("Orientation is: " + str(orientation))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        print(filename)
        file_tmp = cStringIO.StringIO(file.read())
        pil_image = Image.open(file_tmp)
	pil_image = pil_image.resize((pil_image.size[0]/2,pil_image.size[1]/2), Image.ANTIALIAS)

        image_path = UPLOAD_FOLDER + filename
        print("Saving image to: " + image_path + "...\n")
        
        pil_image.save(image_path)
        print("Image saved.\nProcessing text.\n")
        
        if use_matlab:
	    print("Using MATLAB... ")
            text_path = UPLOAD_FOLDER + "output.txt"
            text_path2 = UPLOAD_FOLDER + "output"
            eng.OCRProcessing(image_path, text_path2, orientation, nargout=0)
            
            print("Matlab finished processing.\n")
            text = read_file(text_path)
            
            print("Cleaning text.\n")
            text = ocr.clean_text(text)
            if len(text) < 3:
                print("MATLAB OCR did not give us enough text. Using simple ocr as fallback.\n")
                if orientation != 6:
                    text = ocr.simple_ocr(pil_image)
                else:
                    text = ocr.simple_ocr(pil_image.rotate(-90))
        else:
            print("OCR call (no MATLAB)\n")
            text = ""
            text0 = ocr.simple_ocr(pil_image)
            #text90 = ocr.simple_ocr(pil_image.rotate(90))
            #text = text0 if len(text0) >= len(text90) else text90
            #text180 = ocr.simple_ocr(pil_image.rotate(180))
            #text = text180 if len(text180) > len(text) else text
            #text270 = ocr.simple_ocr(pil_image.rotate(270))
            text270 = ocr.simple_ocr(pil_image.rotate(-90))
            text = text270 if len(text270) > len(text0) else text0
	print("All OCR complete. Cleaned OCR text:\n ")
        print(text)
        return text
    return "Error"

if __name__ == "__main__":
    app.run(debug=True)

