import os
from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from werkzeug.exceptions import BadRequest
import logging

# Import das exceções customizadas do domínio
from errors import PetAppError

# Configura o formato do log (Data, Hora, Nível de erro, Mensagem)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("app_history.log"), # Salva o histórico em arquivo
        logging.StreamHandler()                # Exibe no console
    ]
)

load_dotenv()

# Caminho absoluto para a pasta frontend
BASE_DIR    = os.path.dirname(os.path.abspath(__file__))
FRONTEND    = os.path.join(BASE_DIR, '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND)
CORS(app, resources={r"/api/*": {"origins": "*"}})


# ── Tratadores Globais de Erros ──────────────────────────────

@app.errorhandler(PetAppError)
def handle_pet_app_error(e):
    """
    Captura de forma unificada e limpa qualquer exceção originária do nosso domínio,
    convertendo em respostas JSON limpas e status HTTP semanticamente corretos (502, 503, etc.).
    """
    logging.error(f"Exceção customizada interceptada globalmente [{e.__class__.__name__}]: {e.message}")
    return jsonify({'error': e.message}), e.status_code


@app.errorhandler(BadRequest)
def handle_bad_request(e):
    return jsonify({'error': 'JSON malformado ou requisição inválida.'}), 400


@app.errorhandler(Exception)
def handle_unexpected_error(e):
    # Log detalhado internamente para auditoria e depuração
    logging.error(f"Exceção inesperada capturada no servidor: {str(e)}", exc_info=True)
    return jsonify({'error': 'Ocorreu um erro interno no servidor. Tente novamente mais tarde.'}), 500


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