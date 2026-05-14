from flask import Flask, send_from_directory
from flask_cors import CORS
from routes.pets import pets_bp
from routes.auth import auth_bp
import os

app = Flask(__name__, static_folder='../frontend')
CORS(app)

app.register_blueprint(pets_bp,  url_prefix='/api')
app.register_blueprint(auth_bp,  url_prefix='/api')

@app.route('/')
def index():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def static_files(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
