import os
from flask import Flask, request, jsonify,flash
from werkzeug.utils import secure_filename
from classify_drawing import classify_image
import gc



UPLOAD_FOLDER = './images'
SUGGESTION_FOLDER = './feedback/'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
CONFIDENCE_THRESHOLD = 0.8

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SUGGESTION_FOLDER'] = SUGGESTION_FOLDER

@app.route('/')
def hello_world():
    return 'Hello, World!'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        output = {}
        try:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return ("No file",400)
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return ("No file name",400)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                path = app.config['UPLOAD_FOLDER']
                if not os.path.isdir(path):
                        os.makedirs(path)
                file.save(os.path.join(path, filename))
                drawing_category, confidence = classify_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                if confidence > CONFIDENCE_THRESHOLD:
                    output['category'] = drawing_category
                    output['status'] = 'success'
                else:
                    output['status'] = 'error'
                    output['message'] = 'could not classify the drawing'

        except Exception as e:
            output['status'] = 'error'
            output['message'] = str(e)

        gc.collect()
        return jsonify(output)



@app.route('/failure_feedback',methods=['POST'])
def failure_feedback():
    if request.method == 'POST':
        output = {}
        try:
            # check if the post request has the file part
            if 'file' not in request.files:
                flash('No file part')
                return ("No file",400)
            file = request.files['file']

            if file.filename == '':
                flash('No selected file')
                return ("No file name",400)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                suggested_category = request.form['suggested_category']
                path = app.config['SUGGESTION_FOLDER'] + suggested_category
                if not os.path.isdir(path):
                        os.makedirs(path)
                file.save(os.path.join(path, filename))
                output = {}
                output['status'] = 'success'

        except Exception as e:
                output['status'] = 'error'
                output['message'] = str(e)

        gc.collect()
        return jsonify(output)

if __name__ == '__main__':
      app.run(host='0.0.0.0', port=80)
