import logging
from flask import Blueprint, request, jsonify
from services.supabase_service import register_user, login_user
from errors import DatabaseIntegrationError

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/auth/register', methods=['POST'])
def register():
    logging.info("Rota /auth/register acionada.")
    
    data = request.get_json()
    if not data:
        logging.warning("Tentativa de registro rejeitada: corpo vazio ou inválido.")
        return jsonify({'error': 'Corpo da requisição inválido.'}), 400

    email    = data.get('email', '').strip()
    password = data.get('senha', '').strip()
    metadata = {
        'nome':           data.get('nome', ''),
        'sobrenome':      data.get('sobrenome', ''),
        'telefone':       data.get('telefone', ''),
        'dataNascimento': data.get('dataNascimento', ''),
    }

    if not email or not password:
        logging.warning("Tentativa de registro sem informar email ou senha.")
        return jsonify({'error': 'Email e senha obrigatórios.'}), 400

    if len(password) < 6:
        logging.warning(f"Tentativa de registro com senha muito curta: {email}")
        return jsonify({'error': 'Senha deve ter ao menos 6 caracteres.'}), 400

    try:
        result = register_user(email, password, metadata)
        logging.info(f"Usuário criado com sucesso! ID: {result.get('user_id')}")
        return jsonify({'success': True, **result})
    except ValueError as ve:
        logging.warning(f"Erro de validação de negócios no cadastro: {str(ve)}")
        return jsonify({'error': str(ve)}), 400
    except DatabaseIntegrationError as die:
        # O tratador global em app.py cuida de retornar o erro, mas gravamos o log aqui primeiro
        logging.error(f"Erro de banco durante registro do usuário ({email}): {die.message}", exc_info=True)
        raise die
    except Exception as e:
        logging.error(f"Erro inesperado no cadastro ({email}): {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno inesperado ao cadastrar usuário.'}), 500


@auth_bp.route('/auth/login', methods=['POST'])
def login():
    logging.info("Rota /auth/login acionada.")
    
    data = request.get_json()
    if not data:
        logging.warning("Tentativa de login com corpo da requisição inválido.")
        return jsonify({'error': 'Corpo da requisição inválido.'}), 400

    email    = data.get('email', '').strip()
    password = data.get('senha', '').strip()

    if not email or not password:
        logging.warning("Tentativa de login sem informar credenciais completas.")
        return jsonify({'error': 'Email e senha obrigatórios.'}), 400

    try:
        result = login_user(email, password)
        logging.info(f"Usuário autenticado com sucesso! ID: {result.get('user_id')}")
        return jsonify({'success': True, **result})
    except ValueError as ve:
        logging.warning(f"Falha de credenciais para {email}: {str(ve)}")
        return jsonify({'error': str(ve)}), 401
    except DatabaseIntegrationError as die:
        logging.error(f"Erro de persistência de banco de dados no login de {email}: {die.message}", exc_info=True)
        raise die
    except Exception as e:
        logging.error(f"Erro inesperado no login do usuário {email}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno inesperado ao processar o login.'}), 500