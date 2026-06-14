import base64
import logging
from flask import Blueprint, request, jsonify
from services.ai_service import generate_embedding, pet_vision_analysis
from services.supabase_service import upload_image, register_pet, search_similar_pets, list_pets
from errors import ExternalServiceError, DatabaseIntegrationError

pets_bp = Blueprint('pets', __name__)


@pets_bp.route('/pets', methods=['GET'])
def get_pets():
    logging.info("Rota GET /pets acionada para listar os pets recentes.")
    try:
        pets = list_pets()
        logging.info(f"Lista de pets recuperada com sucesso. Total: {len(pets)} pets.")
        return jsonify(pets)
    except DatabaseIntegrationError as die:
        logging.error(f"Erro ao recuperar listagem de pets do banco: {die.message}", exc_info=True)
        raise die
    except Exception as e:
        logging.error(f"Erro inesperado de servidor no feed de pets: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno ao processar listagem.'}), 500


@pets_bp.route('/pets/search', methods=['POST'])
def search():
    logging.info("Rota POST /pets/search acionada.")
    
    data = request.get_json()
    if not data:
        logging.warning("Tentativa de busca com corpo de requisição vazio ou malformado.")
        return jsonify({'error': 'Corpo da requisição inválido.'}), 400

    image_b64 = data.get('image')
    if not image_b64:
        logging.warning("Tentativa de busca sem enviar imagem.")
        return jsonify({'error': 'Envie uma imagem.'}), 400

    try:
        logging.info("Iniciando geração de embedding visual...")
        embedding = generate_embedding(image_b64)
        
        logging.info("Executando busca de similaridade via pgvector no Supabase...")
        matches = search_similar_pets(embedding, threshold=0.5)
        
        logging.info(f"Busca finalizada. {len(matches)} correspondências encontradas.")
        return jsonify({'matches': matches})
    except (ExternalServiceError, DatabaseIntegrationError) as custom_err:
        logging.error(f"Erro de infraestrutura ({custom_err.__class__.__name__}) na busca: {custom_err.message}", exc_info=True)
        raise custom_err
    except Exception as e:
        logging.error(f"Erro inesperado no fluxo de busca por IA: {str(e)}", exc_info=True)
        return jsonify({'error': 'Falha interna ao processar busca por similaridade.'}), 500


@pets_bp.route('/pets/register', methods=['POST'])
def register():
    logging.info("Rota POST /pets/register acionada.")
    
    image_file = request.files.get('image')
    raca       = request.form.get('raca', '').strip()
    cor        = request.form.get('cor', '').strip()
    cidade     = request.form.get('cidade', '').strip()
    contato    = request.form.get('contato', '').strip()
    descricao  = request.form.get('descricao', '').strip()

    if not cidade:
        logging.warning("Tentativa de cadastro rejeitada: cidade não fornecida.")
        return jsonify({'error': 'Cidade é obrigatória.'}), 400

    if not image_file:
        logging.warning("Tentativa de cadastro rejeitada: imagem não fornecida.")
        return jsonify({'error': 'A imagem do pet é obrigatória para o cadastro.'}), 400

    try:
        logging.info("Fazendo upload da foto para o Supabase Storage...")
        ext = image_file.filename.rsplit('.', 1)[-1].lower() or 'jpg' if image_file.filename else 'jpg'
        file_bytes = image_file.read()
        image_url = upload_image(file_bytes, ext)

        logging.info("Gerando embedding visual nativo com o modelo da NVIDIA...")
        b64 = base64.b64encode(file_bytes).decode('utf-8')
        embedding = generate_embedding(b64)

        pet_data = {
            'species':      raca or 'Desconhecido',
            'breed':        raca,
            'color':        cor,
            'description':  descricao,
            'lastLocation': cidade,
            'contactInfo':  contato,
            'imageUrl':     image_url,
            'embedding':    embedding,
        }

        logging.info("Persistindo o pet com o novo vetor no Supabase...")
        result = register_pet(pet_data)
        
        logging.info(f"Pet cadastrado com sucesso! ID: {result.get('id')}")
        return jsonify({'success': True, 'pet': result})
    except (ExternalServiceError, DatabaseIntegrationError) as custom_err:
        logging.error(f"Erro de infraestrutura ao cadastrar pet: {custom_err.message}", exc_info=True)
        raise custom_err
    except Exception as e:
        logging.error(f"Erro de sistema ao registrar o pet: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno ao processar cadastro do pet.'}), 500


@pets_bp.route('/pets/analyze', methods=['POST'])
def analyze():
    logging.info("Rota POST /pets/analyze acionada.")
    
    data = request.get_json()
    if not data:
        logging.warning("Tentativa de análise com corpo de requisição malformado.")
        return jsonify({'error': 'Corpo da requisição inválido.'}), 400

    image_b64 = data.get('image')
    if not image_b64:
        logging.warning("Tentativa de pré-análise sem a imagem em base64.")
        return jsonify({'error': 'Imagem obrigatória.'}), 400

    try:
        logging.info("Fazendo chamada de análise visual do modelo Vision...")
        analysis = pet_vision_analysis(image_b64)
        logging.info("Análise concluída com sucesso.")
        return jsonify(analysis)
    except ExternalServiceError as ese:
        logging.error(f"Falha de IA ao analisar imagem: {ese.message}", exc_info=True)
        raise ese
    except Exception as e:
        logging.error(f"Erro interno de rotas na análise de imagem: {str(e)}", exc_info=True)
        return jsonify({'error': 'Falha ao analisar a imagem do pet.'}), 500