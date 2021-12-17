from flask import Flask, request, make_response, flash, redirect
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from flask.json import jsonify
app = Flask(__name__)
initial_time = datetime.today()

@app.route('/')
def index():
    return jsonify(Saludo="Hi!")


@app.route('/health')
def health():
       
    execution_time = datetime.today() - initial_time
    times = {
        "today":datetime.today().strftime('%d/%m/%Y %H:%M:%Ss'),
        "execution_time":  str(execution_time)
    }
    return make_response(jsonify(times), 202)
    

@app.route('/sayhello', methods=['POST'])
def sayhello():
    res =  request.get_json()
    if res['mensaje'] == 'hello':
        return "Hola mundo!"

@app.route('/gatos')
def gatos():
    return ""


@app.route('/perros')
def perros():
    return ""

@app.route('/image', methods= ['POST'])
def uploadFile():
    if request.method == 'POST':

        # Check if there is a multipart element called 'file'
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({"error": "Wrong extension."}), 400

        # Check if file has name
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return jsonify({"error": "Can't find that file."}), 404

        # Check if file exist and extension.
        if file and file.filename:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return jsonify({'msg': "File uploaded."}), 201
        else:
            return jsonify({"error": "Wrong extension or inexistent file."}), 405

