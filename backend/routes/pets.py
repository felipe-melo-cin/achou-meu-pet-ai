import base64
from flask import Blueprint, request, jsonify
from services.ai_service import generate_embedding, pet_vision_analysis
from services.supabase_service import upload_image, register_pet, search_similar_pets

pets_bp = Blueprint('pets', __name__)


@pets_bp.route('/pets/search', methods=['POST'])
def search():
    """Busca pets similares a partir de imagem e/ou descrição."""
    data = request.get_json()
    image_b64 = data.get('image')       # base64 puro (sem prefixo data:...)
    description = data.get('description', '').strip()

    if not image_b64 and not description:
        return jsonify({'error': 'Envie uma imagem ou descrição.'}), 400

    try:
        if image_b64:
            embedding = generate_embedding(image_b64)
        else:
            # Fallback: embedding por texto
            from openai import OpenAI
            import os
            client = OpenAI(
                base_url="https://openrouter.ai/api/v1",
                api_key=os.environ.get("OPENROUTER_API_KEY"),
            )
            res = client.embeddings.create(
                model="openai/text-embedding-3-small",
                input=description,
            )
            embedding = res.data[0].embedding

        matches = search_similar_pets(embedding, threshold=0.5)
        return jsonify({'matches': matches})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pets_bp.route('/pets/register', methods=['POST'])
def register():
    """Cadastra um pet encontrado."""
    data = request.form
    image_file = request.files.get('image')

    animal   = data.get('animal', '').strip()
    regiao   = data.get('regiao', '').strip()
    descricao = data.get('descricao', '').strip()

    if not animal or not regiao:
        return jsonify({'error': 'Animal e região são obrigatórios.'}), 400

    try:
        image_url = ''
        embedding = []

        if image_file:
            ext = image_file.filename.rsplit('.', 1)[-1].lower()
            file_bytes = image_file.read()
            image_url = upload_image(file_bytes, ext)

            # Gera embedding a partir do base64 da imagem
            b64 = base64.b64encode(file_bytes).decode('utf-8')
            embedding = generate_embedding(b64)

        pet_data = {
            'species':      animal,
            'breed':        '',
            'color':        '',
            'description':  descricao,
            'lastLocation': regiao,
            'contactInfo':  data.get('contato', ''),
            'imageUrl':     image_url,
            'embedding':    embedding,
        }

        result = register_pet(pet_data)
        return jsonify({'success': True, 'pet': result})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@pets_bp.route('/pets/analyze', methods=['POST'])
def analyze():
    """Analisa imagem com IA e retorna descrição automática."""
    data = request.get_json()
    image_b64 = data.get('image')

    if not image_b64:
        return jsonify({'error': 'Imagem obrigatória.'}), 400

    try:
        result = pet_vision_analysis(image_b64)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500
