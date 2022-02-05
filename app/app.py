from flask import Flask, request, make_response, flash, redirect,send_from_directory
from datetime import datetime
from werkzeug.utils import secure_filename
import os
from datetime import datetime
from flask.json import jsonify
from utils import *



app = Flask(__name__)
initial_time = datetime.today()




# Upload pre configuration
folderName = 'uploads'
uploadFolder = './' + folderName
alowedExtensions = {'png'}

if not os.path.exists(uploadFolder):
    os.makedirs(uploadFolder)


# Endpoint de entrada
@app.route('/')
def index():
    return jsonify(Saludo="Hi!")

# Endpoint Healthcheck. Donde devolvemos el tiempo que lleva en marcha el servidor.
@app.route('/healthcheck')
def health():
       
    execution_time = datetime.today() - initial_time
    times = {
        "today":datetime.today().strftime('%d/%m/%Y %H:%M:%Ss'),
        "execution_time":  str(execution_time)
    }
    return make_response(jsonify(times), 202)
    

@app.route('/hola', methods=['POST'])
def hola():
    res =  request.get_json()
    return "Hola " + res["name"] + "!!"


@app.route("/file", methods=["POST"])
def uploadFile():
    if request.method == 'POST':
     
        # Miramos si el usuario nos pasa un un archivo (tipo file)
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({"error": "Wrong extension."}), 400
        
        # Miramos si tiene un nombre el archivo
        file = request.files['file']
        if file.filename == '':
            flash('No hay foto!')
            return jsonify({"error": "No puedo encontrar la foto :("}), 404

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


@app.route("/file-view/<path:filename>", methods=["GET"])
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