import base64
import logging  # <-- Importa o módulo de logs
from flask import Blueprint, request, jsonify
from services.ai_service import generate_embedding, pet_vision_analysis
from services.supabase_service import upload_image, register_pet, search_similar_pets, list_pets

pets_bp = Blueprint('pets', __name__)


@pets_bp.route('/pets', methods=['GET'])
def get_pets():
    # Histórico de chamada da API
    logging.info("Rota GET /pets acionada para listar os pets recentes.")
    try:
        pets = list_pets()
        logging.info(f"Lista de pets recuperada com sucesso. Total: {len(pets)} pets.")
        return jsonify(pets)
    except Exception as e:
        # Registra o erro de infraestrutura interno mas protege o usuário externo
        logging.error(f"Erro ao listar pets do banco: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno ao recuperar o feed de pets.'}), 500


@pets_bp.route('/pets/search', methods=['POST'])
def search():
    logging.info("Rota POST /pets/search acionada.")
    
    data = request.get_json()
    if not data:
        logging.warning("Tentativa de busca com corpo de requisição vazio ou malformado.")
        return jsonify({'error': 'Corpo da requisição inválido.'}), 400

    image_b64 = data.get('image')
    if not image_b64:
        logging.warning("Tentativa de busca de similaridade realizada sem enviar imagem.")
        return jsonify({'error': 'Envie uma imagem.'}), 400

    try:
        logging.info("Iniciando geração de embedding para busca...")
        embedding = generate_embedding(image_b64)
        
        logging.info("Executando busca por similaridade de vetores no Supabase...")
        matches = search_similar_pets(embedding, threshold=0.5)
        
        logging.info(f"Busca finalizada. {len(matches)} correspondências encontradas.")
        return jsonify({'matches': matches})
    except Exception as e:
        logging.error(f"Erro durante o processo de busca por IA/Similaridade: {str(e)}", exc_info=True)
        return jsonify({'error': 'Falha interna ao processar a busca por similaridade.'}), 500


@pets_bp.route('/pets/register', methods=['POST'])
def register():
    logging.info("Rota POST /pets/register acionada.")
    
    # Tratando entrada de formulário multipart
    image_file = request.files.get('image')
    raca       = request.form.get('raca', '').strip()
    cor        = request.form.get('cor', '').strip()
    cidade     = request.form.get('cidade', '').strip()
    contato    = request.form.get('contato', '').strip()
    descricao  = request.form.get('descricao', '').strip()

    # Validação de Entrada Malformada / Campos Obrigatórios
    if not cidade:
        logging.warning("Tentativa de cadastro rejeitada: cidade não informada.")
        return jsonify({'error': 'Cidade é obrigatória.'}), 400

    if not image_file:
        logging.warning("Tentativa de cadastro rejeitada: nenhuma imagem enviada.")
        return jsonify({'error': 'A imagem do pet é obrigatória para o cadastro.'}), 400

    try:
        logging.info(f"Iniciando upload da imagem para o pet na cidade {cidade}...")
        ext        = image_file.filename.rsplit('.', 1)[-1].lower() or 'jpg' if image_file.filename else 'jpg'
        file_bytes = image_file.read()
        image_url  = upload_image(file_bytes, ext)
        logging.info("Upload de imagem concluído com sucesso.")

        logging.info("Gerando análise de IA e vetores (embeddings) para o novo pet...")
        b64        = base64.b64encode(file_bytes).decode('utf-8')
        embedding  = generate_embedding(b64)

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

        logging.info("Salvando dados filtrados no banco de dados Supabase...")
        result = register_pet(pet_data)
        
        logging.info(f"Pet cadastrado com sucesso! ID gerado no banco: {result.get('id')}")
        return jsonify({'success': True, 'pet': result})

    except Exception as e:
        logging.error(f"Erro crítico ao registrar novo pet: {str(e)}", exc_info=True)
        return jsonify({'error': 'Erro interno ao processar o cadastro do pet.'}), 500


@pets_bp.route('/pets/analyze', methods=['POST'])
def analyze():
    logging.info("Rota POST /pets/analyze acionada.")
    
    data = request.get_json()
    if not data:
        logging.warning("Tentativa de análise com corpo de requisição malformado.")
        return jsonify({'error': 'Corpo da requisição inválido.'}), 400

    image_b64 = data.get('image')
    if not image_b64:
        logging.warning("Tentativa de pré-análise sem fornecer a imagem em base64.")
        return jsonify({'error': 'Imagem obrigatória.'}), 400

    try:
        logging.info("Enviando imagem para análise visual do modelo de IA...")
        analysis = pet_vision_analysis(image_b64)
        logging.info("Análise da IA concluída com sucesso.")
        return jsonify(analysis)
    except Exception as e:
        logging.error(f"Erro na comunicação ou processamento da IA Vision: {str(e)}", exc_info=True)
        return jsonify({'error': 'Falha ao analisar a imagem do pet utilizando Inteligência Artificial.'}), 500