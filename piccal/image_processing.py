from werkzeug import secure_filename
from PIL import Image
import cStringIO
import ocr

def preprocess_image(image):
    image.filter(ImageFilter.SHARPEN)
    image = reduce_if_needed(image)

def reduce_if_needed(image)
    return image.resize((pil_image.size[0]/2,pil_image.size[1]/2), Image.ANTIALIAS)

def read_file(text_path):
    with open(text_path, 'r') as f:
        read_data = f.read()
        return read_data

class OCRImage(object):
    def __init__(self, file, orientation):
        self.filename = secure_filename(file.filename)
        
        file_tmp = cStringIO.StringIO(file.read())
        self.image = Image.open(file_tmp)
        self.image = preprocess_image(self.image)
        self.orientation = orientation
        
    def save(self, folder):
        print("Saving image to: " + image_path + "...\n")
        path = folder + self.filename
        self.image_path = path
        self.image.save(path)
        
    def simple_ocr(self):
        if self.orientation != 6:
            text = ocr.simple_ocr(self.image)
        else:
            text = ocr.simple_ocr(self.image.rotate(-90))
        return text
        
    def matlab_ocr(self, matlab_eng, UPLOAD_FOLDER, corners):
        text_path = UPLOAD_FOLDER + "output.txt"
        text_path2 = UPLOAD_FOLDER + "output"
        matlab_eng.OCRProcessing(self.image_path, text_path2, self.orientation, nargout=0)

        print("Matlab finished processing.\n")
        text = read_file(text_path)

        print("Cleaning text.\n")
        text = ocr.clean_text(text)