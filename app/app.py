from crypt import methods
from flask import Flask, request, make_response, flash, redirect,send_from_directory, abort
from datetime import datetime
from werkzeug.utils import secure_filename
import os, json
from datetime import datetime
from flask.json import jsonify
from utils import *



app = Flask(__name__)
app.use_x_sendfile = True



# Pongo aquí la fecha y hora actual, ya que es cuando se carga la APP (es decir la aplicación Flask)
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
     
        # Miramos si el usuario nos pasa un un archivo (tipo file), y devolvemos un error 400
        if 'file' not in request.files:
            flash('No file part')
            return jsonify({"error": "Extensión incorrecta."}), 400
        
        # Miramos si tiene un nombre el archivo, sino devolvemos un error 404
        file = request.files['file']
        if file.filename == '':
            flash('No hay foto!')
            return jsonify({"error": "No puedo encontrar la foto :( "}), 404

        # Check if file exist and extension.
        if file and allowedFile(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(uploadFolder, filename))
            return jsonify({'msg': "Fichero subido!"}), 201
        else:
            return jsonify({"error": "Error con el fichero"}), 405


# A pesar de activar X-Sendfile no funciona la descarga en mi equipo
@app.route("/descargar/<path:filename>", methods=["GET"])
def downloadFile(filename):            
    downloadTarget = os.path.join(app.root_path, folderName)    
    try:
        return send_from_directory(directory=downloadTarget, path=filename, as_attachment=True)
    except FileNotFoundError:        
        abort(404)


# Endpoint que devuelve un json
@app.route("/json", methods=["GET"])
def damejson():
    # Leo el fichero json de la carpeta uploads, y después lo devuelvo
    f = open('./uploads/FACES_API.json')
    data = json.load(f)
    return jsonify(data)



# Función para calcular el tiempo transcurrido en segundos
def current_milli_time():
    return round(datetime.time() * 1000)

def allowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in alowedExtensions