import logging  # <-- Importa o módulo de logs
from flask import Blueprint, request, jsonify
from services.supabase_service import register_user, login_user

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    # Histórico de chamada da API
    logging.info("Rota /auth/register acionada.")
    
    data = request.get_json()
    
    # Validação para evitar que o backend quebre se o JSON vier vazio/malformado
    if not data:
        logging.warning("Tentativa de registro com corpo da requisição vazio ou malformado.")
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
        logging.warning(f"Tentativa de registro com senha muito curta para o email: {email}")
        return jsonify({'error': 'Senha deve ter ao menos 6 caracteres.'}), 400

    try:
        result = register_user(email, password, metadata)
        logging.info(f"Usuário criado com sucesso! ID: {result.get('user_id')}")
        return jsonify({'success': True, **result})
    except Exception as e:
        # Grava o erro real com o traceback completo no arquivo de log
        logging.error(f"Erro ao registrar usuário ({email}): {str(e)}", exc_info=True)
        # Retorna uma mensagem genérica e segura para a API cliente
        return jsonify({'error': 'Erro interno ao processar o cadastro.'}), 500


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
        logging.warning("Tentativa de login sem informar as credenciais.")
        return jsonify({'error': 'Email e senha obrigatórios.'}), 400

    try:
        result = login_user(email, password)
        logging.info(f"Usuário autenticado com sucesso! ID: {result.get('user_id')}")
        return jsonify({'success': True, **result})
    except ValueError as ve:
        # Erros esperados de negócio (ex: senha incorreta) geram um warning
        logging.warning(f"Falha de autenticação para o usuário {email}: {str(ve)}")
        return jsonify({'error': str(ve)}), 401  # Mudado para 401 (Não autorizado) que faz mais sentido que 500
    except Exception as e:
        # Erros inesperados de sistema (banco fora do ar, erro de rede, etc) geram um error
        logging.error(f"Erro inesperado no login do usuário {email}: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno ao processar o login.'}), 500