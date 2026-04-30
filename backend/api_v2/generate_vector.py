from Models import ImageUrlToVectorModel

# O modelo de embedding é gerado
model = ImageUrlToVectorModel("nvidia/llama-nemotron-embed-vl-1b-v2:free")

# O usuário fornece um url de imagem
message = input("> ")

# O modelo gera um vetor de números reais com base no url de imagem fornecido
vector = model.generate_image_vector(message)

# O vetor é enviado para processamento posterior
print(vector)
