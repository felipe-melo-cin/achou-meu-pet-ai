import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

load_dotenv()

# Caminho absoluto para a pasta frontend
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
FRONTEND    = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND)
CORS(app)

# ── Blueprints ──────────────────────────────────────────
from routes.pets  import pets_bp
from routes.auth  import auth_bp

app.register_blueprint(pets_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api')

# ── Serve frontend ───────────────────────────────────────
@app.route('/')
def index():
    return send_from_directory(FRONTEND, 'index.html')

@app.route('/<path:path>')
def static_files(path):
    full = os.path.join(FRONTEND, path)
    if os.path.isfile(full):
        return send_from_directory(FRONTEND, path)
    # SPA fallback — qualquer rota desconhecida devolve index.html
    return send_from_directory(FRONTEND, 'index.html')

# ── Rota de saúde ────────────────────────────────────────
@app.route('/api/health')
def health():
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
