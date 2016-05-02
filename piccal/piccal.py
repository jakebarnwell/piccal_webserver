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
    #log_file.close()
    log_file.write(str(request.files)+"\n")
    log_file.write(str(request.files['file'].headers)+"\n")
    file = request.files['file']
    if file and allowed_file(file.filename):
        #with open("/tmp/manual_copy.bmp","wb") as f:
        #    f.write(file.read())
	#file.save("/tmp/file_save.txt")	
#with open("/tmp/manual_text.txt","w") as f:
	#    f.write(file.stream.read())
        log_file.write("save image\n")
        #request.files['file'].save('/tmp/bitmap.bmp')
        log_file.write("Processing File\n")
        filename = secure_filename(file.filename)
        #file.save(os.path.join("/tmp", "test_" + filename))
        log_file.write("Got filename\n")
        file_tmp = cStringIO.StringIO(file.read())
        #log_file.write("Type " + str(type(file.read())) + "\n")
        pil_image = Image.open(file_tmp)
        log_file.write("Read image\n")
        pil_image.save("/tmp/PIL_saved_image.jpg")
        log_file.write("Image saved.\n")
#        text = ocr.simple_ocr(pil_image)
        text = "this is test text"
        text_file = open("/tmp/output.txt", "w")
        text_file.write(text)
	text_file.close()
        eng = matlab.engine.start_matlab()
        eng.OCRProcessing("input_path_img", "output_path_text")
        #cv2_image = convert_to_cv(file.read())
        #extracted_texts, bboxes = ocr.extract_image_text(cv2_image)
        print(text)
        log_file.write("Success writing text\n")
        log_file.close()
        return text
    return "Error"

if __name__ == "__main__":
    app.run(debug=True)

