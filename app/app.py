from flask import Flask, request, Response
from datetime import datetime

from flask.json import jsonify
app = Flask(__name__)
initial_time = datetime.today()

@app.route('/')
def index():
    return jsonify("Hi!")


@app.route('/health')
def health():
       
    execution_time = datetime.today() - initial_time
    times = {
        "today":datetime.today().strftime('%d/%m/%Y %H:%M:%Ss'),
        "execution_time":  str(execution_time)
    }
    return Response(jsonify(times), status=202)
    

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

@app.route('/image/<imagen>')
def image(imagen):
    return ""

