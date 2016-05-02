import cStringIO
import os
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
#import cv2
from PIL import Image
from StringIO import StringIO
import numpy as np
import matlab.engine
#import ocr

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
    print("Post request received")
    
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_tmp = cStringIO.StringIO(file.read())
        pil_image = Image.open(file_tmp)
        
        image_path = UPLOAD_FOLDER + "PIL_saved_image.jpg"
        print("Saving image to: " + image_path)
        
        pil_image.save(image_path)
        print("Image saved.\n Processing text.")
        
        text_path = UPLOAD_FOLDER + "output.txt"
        eng.OCRProcessing(image_path, text_path, nargout=0)
        text = read_file(text_path)
        print(text)
        log_file.write("Success writing text\n")
        log_file.close()
        return text
    return "Error"

if __name__ == "__main__":
    eng = matlab.engine.start_matlab()
    app.run(debug=True)
    eng.quit()

