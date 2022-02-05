from app.app import app
import os


UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = set(['png'])


secret_key = os.urandom(24)

app.config['SECRET_KEY'] = secret_key

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS



if __name__ == "__main__":
    app.run(port=5001, debug=True)
