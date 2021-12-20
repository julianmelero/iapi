from flask import Flask, request, make_response, flash, redirect
from datetime import datetime
from werkzeug.utils import secure_filename, send_from_directory
import os
from datetime import datetime
from flask.json import jsonify
from utils import *



app = Flask(__name__)
initial_time = datetime.today()




# Upload pre configuration
folderName = 'uploads'
uploadFolder = './' + folderName
alowedExtensions = {'jpg', 'png', 'jpeg', 'gif'}

if not os.path.exists(uploadFolder):
    os.makedirs(uploadFolder)



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

@app.route("/file", methods=["POST"])
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
        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(uploadFolder, filename))
            return jsonify({'msg': "File uploaded."}), 201
        else:
            return jsonify({"error": "Wrong extension or inexistent file."}), 405


@app.route("/file/<path:filename>", methods=["GET"])
def downloadFile(filename):
    downloadTarget = os.path.join(app.root_path, folderName)
    print(downloadTarget)
    return send_from_directory(directory=uploadFolder, path=filename, as_attachment=True)


app.route("/file-view/<path:filename>", methods=["GET"])
def viewFile(filename):
    downloadTarget = os.path.join(app.root_path, folderName)
    print(downloadTarget)
    return send_from_directory(directory=uploadFolder, path=filename, as_attachment=False)

# Request other API
@app.route("/external", methods=["GET"])
def checkOtherAPI():
    response = request.data("http://api.open-notify.org/astros.json")
    return response.content, response.status_code




def current_milli_time():
    return round(datetime.time() * 1000)

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in alowedExtensions