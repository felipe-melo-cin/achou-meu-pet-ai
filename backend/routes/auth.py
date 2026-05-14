from flask import Blueprint, request, jsonify
from services.supabase_service import register_user, login_user

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    email    = data.get('email', '').strip()
    password = data.get('senha', '').strip()
    metadata = {
        'nome':           data.get('nome', ''),
        'sobrenome':      data.get('sobrenome', ''),
        'telefone':       data.get('telefone', ''),
        'dataNascimento': data.get('dataNascimento', ''),
    }

    if not email or not password:
        return jsonify({'error': 'Email e senha obrigatórios.'}), 400

    if len(password) < 6:
        return jsonify({'error': 'Senha deve ter ao menos 6 caracteres.'}), 400

    try:
        result = register_user(email, password, metadata)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email    = data.get('email', '').strip()
    password = data.get('senha', '').strip()

    if not email or not password:
        return jsonify({'error': 'Email e senha obrigatórios.'}), 400

    try:
        result = login_user(email, password)
        return jsonify({'success': True, **result})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
