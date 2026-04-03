from openai import OpenAI
import os
import dotenv
import backend.api.interface as interface

# Carrega as variáveis de ambiente
dotenv.load_dotenv()

# Coleta a chave da API nas variáveis de ambiente
MODEL_API_KEY = os.getenv("MODEL_API_KEY")

# Gera o cliente com base na chave da API
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=MODEL_API_KEY,
)

chat_log = []
image_path = None

while True:

    message = input("> ")

    # O usuário deseja enviar uma imagem além do texto
    if message == "image":
        image_path = input("Insert image path > ")
        encoded_image = interface.base64_encode(image_path)
        continue

    # O usuário deseja sair
    if message == "exit":
        break

    # Mensagem vem com imagem ou sem imagem
    if image_path:
        interface.send_image(chat_log, message, encoded_image)
        image_path = None
    else:
        interface.send_message(chat_log, message)

    # Resposta do modelo é registrada e enviada para o histórico de conversa
    response = interface.generate_response(client, chat_log)
    answer = response.output_text
    interface.send_message(chat_log, answer)

    print('\033[31mAnswer:\033[m', answer)
