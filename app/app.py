from flask import Flask
from datetime import datetime
app = Flask(__name__)


@app.route('/')
def index():
    return "Hi!"


@app.route('/health')
def health():    
    return datetime.today().strftime('%d/%m/%Y %H:%M:%S')

