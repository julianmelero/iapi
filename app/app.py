from flask import Flask, request
from datetime import datetime
app = Flask(__name__)
initial_time = datetime.today()

@app.route('/')
def index():
    return "Hi!"


@app.route('/health')
def health():    
    execution_time = datetime.today() - initial_time
    return "Today is " + datetime.today().strftime('%d/%m/%Y %H:%M:%S') + "\n Server execution time:" +  str(execution_time)

@app.route('/sayhello', methods=['POST'])
def sayhello():
    res =  request.get_json()
    if res['mensaje'] == 'hello':
        return "Hola mundo!"