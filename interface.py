from base64 import b64encode

def send_message(conversation, content):
    """Envia uma mensagem para o histórico de conversa com a IA"""
    conversation.append({"role": "user", "content": content})

def send_image(conversation, text_content, image_content):
    """Envia uma mensagem acompanhada de uma imagem para o histórico de conversa com a IA"""
    conversation.append({
        "role": "user",
        "content": [
            {"type": "input_text", "text": text_content},
            {"type": "input_image", "image_url": f"data:image/jpeg;base64,{image_content}"},
        ]
    })

def generate_response(client, conversation):
    """Gera uma nova mensagem com base no histórico de conversa"""
    return client.responses.create(
        model="nvidia/nemotron-nano-12b-v2-vl:free",
        input=conversation,
    )

def register_model_response(conversation, content):
    """Insere uma resposta gerada pelo modelo no histórico de conversa"""
    conversation.append({"role": "assistant", "content": content})

def base64_encode(image):
    """Converte a imagem fornecida para base64, necessário para o modelo"""
    with open(image, "rb") as image_file:
        return b64encode(image_file.read()).decode('utf-8')
