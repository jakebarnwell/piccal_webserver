from werkzeug import secure_filename
from PIL import Image, ImageFilter
import cStringIO
import ocr
import unicodedata

def preprocess_image(image, orientation):
    image.filter(ImageFilter.SHARPEN)
    image = fix_orientation(image, orientation)
    #image = reduce_if_needed(image)
    return image

def fix_orientation(image, orientation):
    if orientation == 3:
        image = image.rotate(180)
    elif orientation == 6:
        image = image.rotate(270)
    elif orientation == 8:
        image = image.rotate(90)
    return image

def reduce_if_needed(image):
    return image.resize((image.size[0]/2, image.size[1]/2), Image.ANTIALIAS)

def read_file(text_path):
    with open(text_path, 'r') as f:
        read_data = f.read()
        return read_data

def average_word_count(ocr_output):
    num_words = len(ocr_output.split())
    num_chars = sum([1 for c in ocr_output if c != " "])
    if num_words == 0:
        num_words = 1
    return num_chars*1.0/num_words

class OCRImage(object):
    def __init__(self, file, orientation):
        self.filename = secure_filename(file.filename)
        file_tmp = cStringIO.StringIO(file.read())
        self.image = Image.open(file_tmp)
        self.image = preprocess_image(self.image, orientation)
        self.orientation = orientation
        
        
    def save(self, folder):
        path = folder + self.filename
        self.image_path = path
        self.image.save(path)
        print("Image saved to path " + path +"\n")
        
    def simple_ocr(self):
        text = ocr.simple_ocr(self.image)
        return text
        
    def matlab_ocr(self, matlab_eng, UPLOAD_FOLDER, corners):
        text_path = UPLOAD_FOLDER + "output.txt"
        text_path2 = UPLOAD_FOLDER + "output"
        
        print("here")
        width = self.image.size[0]
        height = self.image.size[1]
        print(width)
        print(height)
        #for i in range(4):
        #    corners[2*i] = corners[2*i]*width
        #    print(corners[2*i])
        #    corners[2*i+1] = corners[2*i+1]* height
        #    print(corners[2*i+1])

        (output_str) = matlab_eng.textDetection(self.image_path, corners[0], corners[1], corners[2], corners[3], corners[4], corners[5], corners[6], corners[7], nargout = 1)
        if type(output_str) is str:
		ocr_str = output_str
	else:
        	ocr_str = unicodedata.normalize('NFKD', output_str).encode('ascii', 'ignore')

        print(ocr_str)
        clean_text_str = ocr.clean_text(ocr.clean_text(ocr_str))
        print(clean_text_str)
        
        
        
        #if average_word_count(clean_text_1) > average_word_count(clean_text_2):
        #    text = clean_text_1
        #else:
        #    text = clean_text_2
         #matlab_eng.OCRProcessing(self.image_path, text_path2, self.orientation, nargout=0)
        return clean_text_str

#        print("Matlab finished processing.\n")
#        text = read_file(text_path)
#
#        print("Cleaning text.\n")
#        text = ocr.clean_text(text)
