from app.app import app



UPLOAD_FOLDER = "./images"
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])



app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = ALLOWED_EXTENSIONS


app.config['DEBUG'] = True


if __name__ == "__main__":
    app.run()
