import base64
from flask import Blueprint, request, jsonify
from services.ai_service import generate_embedding, pet_vision_analysis
from services.supabase_service import upload_image, register_pet, search_similar_pets, list_pets

pets_bp = Blueprint('pets', __name__)


@pets_bp.route('/pets', methods=['GET'])
def get_pets():
    try:
        pets = list_pets()
        return jsonify(pets)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pets_bp.route('/pets/search', methods=['POST'])
def search():
    data      = request.get_json()
    image_b64 = data.get('image')

    if not image_b64:
        return jsonify({'error': 'Envie uma imagem.'}), 400

    try:
        embedding = generate_embedding(image_b64)
        matches   = search_similar_pets(embedding, threshold=0.5)
        return jsonify({'matches': matches})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pets_bp.route('/pets/register', methods=['POST'])
def register():
    image_file = request.files.get('image')
    # Colunas reais da tabela: species, breed, color, description, lastLocation, contactInfo, imageUrl, embedding
    raca      = request.form.get('raca', '').strip()
    cor       = request.form.get('cor', '').strip()
    cidade    = request.form.get('cidade', '').strip()
    descricao = request.form.get('descricao', '').strip()
    contato   = request.form.get('contato', '').strip()

    if not cidade:
        return jsonify({'error': 'Cidade é obrigatória.'}), 400

    try:
        image_url = ''
        embedding = []

        if image_file:
            ext        = image_file.filename.rsplit('.', 1)[-1].lower() or 'jpg'
            file_bytes = image_file.read()
            image_url  = upload_image(file_bytes, ext)
            b64        = base64.b64encode(file_bytes).decode('utf-8')
            embedding  = generate_embedding(b64)

        pet_data = {
            'species':      raca or 'Desconhecido',
            'breed':        raca,
            'color':        cor,           # coluna correta: color
            'description':  descricao,
            'lastLocation': cidade,
            'contactInfo':  contato,
            'imageUrl':     image_url,
            'embedding':    embedding,
            # NÃO inclui: size, foundDate, status (não existem na tabela)
        }

        result = register_pet(pet_data)
        return jsonify({'success': True, 'pet': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pets_bp.route('/pets/analyze', methods=['POST'])
def analyze():
    data      = request.get_json()
    image_b64 = data.get('image')

    if not image_b64:
        return jsonify({'error': 'Imagem obrigatória.'}), 400

    try:
        result = pet_vision_analysis(image_b64)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
