from ocr import *
from flask import Flask, request, jsonify
app = Flask(__name__)

_VERSION = 1

@app.route('/')
def hi():
    return "Hello world!"

@app.route('/v{}/ocr_api'.format(_VERSION), methods=['POST'])
def upload_files():
    resp = flask.make_response()
    if request.files['image']:
        image = request.files['image']
        resp.status_code = 204
    else:
        resp.status_code = 411
    return resp

@app.route('/v{}/ocr'.format(_VERSION), methods=["POST"])
def ocr():
    try:
        url = request.json['image_url']
        if 'jpg' in url:
            output = process_image(url)
            return jsonify({"output": output})
        else:
            return jsonify({"error": "only .jpg files, please"})
    except:
        return jsonify(
            {"error": "Did you mean to send: {'image_url': 'some_jpeg_url'}"}
        )
    
if __name__ == '__main__':
    app.run()