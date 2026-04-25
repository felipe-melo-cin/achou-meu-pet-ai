# 🐾 Achou Meu Pet AI?

> **Transformando fotos em reencontros através de Inteligência Artificial Multimodal.**

O **Achou Meu Pet AI?** é uma plataforma centralizada para auxiliar na localização de animais perdidos. O projeto resolve a ineficiência das redes sociais tradicionais ao utilizar modelos de Visão Computacional para identificar características de animais e busca vetorial para encontrar "matchs" de similaridade entre pets perdidos e encontrados.

---
## 🚀 O Diferencial Tecnológico: Fluxo de IA

Diferente de fóruns comuns, nossa aplicação automatiza a descrição e a busca:

1. **Visão (Image-to-Text):** O modelo **NVIDIA Nemotron-70B** analisa a foto e gera uma descrição técnica e objetiva (espécie, cor, porte, marcas).

2. **Vetorização (Embedding):** Essa descrição é convertida em um vetor matemático (lista de números).

3. **Busca Vetorial (Match Score):** Comparamos o vetor do animal procurado com o banco de dados usando **Similaridade por Cosseno**.

4. **Limiar de 70%:** O sistema apenas sugere ao usuário animais que possuam mais de **70% de similaridade** visual e descritiva, filtrando ruídos e aumentando a precisão.

---

## 📂 Estrutura do Repositório

```bash
/achou-meu-pet-ai
├── /frontend              # Flet
│   ├── /screens     	   # Páginas (Home, Pesquisar, Cadastrar)
│   ├── /componentes	   # Widgets reutilizáveis
│   ├── theme.py     	   # Temas, cores, constantes de UI
│	├── router.py          # Navegação entre as telas
│	└── __init__.py
│
├── /backend			   # Funções Python
│   ├── /ai	
│	│	├── __init__.py  
│   │	├── config.py 	   # Configs OpenRouter
│   │	├── base.py	       # O BaseModel
│	│	├── embeddings.py  # ImageUrlToVectorModel
│   │   ├── vision.py      # Análise de imagem
│	│	└── pipeline.py    # Orquestra vision + embeddings
│   └── /database
│		├── __init__.py    
│		├── client.py      # Cliente Supabase
│		├── queries.py     # Querys do BD
│		├── storage.py     # Gerenciar armazenamento
│		└── models.py	   # Schemas/tipos 
│
├── main.py                # Ponto de entrada (Roda o App Flet)
├── docker-compose.yml     # Orquestração de ambiente local
├── CONTRIBUTING.md		   # Documento de contribuição no projeto
└── README.md              # Visão geral do projeto
```
---

## 🛠️ Instalação e Execução Local

Como o projeto ainda não está em deploy, siga os passos abaixo para rodar o ambiente de desenvolvimento:
### 1. Pré-requisitos

- *Docker* e *Docker Compose* instalados.
- *Node.js* (v18+)
- *Python* (3.10+)
- Chaves de API: *OpenRouter* (Nemotron) e *Supabase*.

### 2. Configuração de Variáveis de Ambiente

Crie um arquivo `.env` com as seguintes chaves:

```Env
OPENROUTER_API_KEY=sua_chave_aqui
EMBEDDING_MODEL_KEY=sua_chave_aqui
SUPABASE_URL=sua_url_supabase
SUPABASE_KEY=sua_chave_anon_public
```

### 3. Subindo a Aplicação

Execute o comando abaixo na raiz do projeto:

```bash
docker-compose up --build
```

- **Frontend:** Disponível em http://localhost:3000
- **Backend (API):** Disponível em http://localhost:8000
- **Documentação API (Swagger):** http://localhost:8000/docs
---

## 👥 Equipe e Divisão de Papéis

O projeto é desenvolvido por uma equipe de 6 integrantes, com papéis rotativos para garantir o aprendizado em todas as frentes:
### Integrantes:

- Arthur Araújo
- Bianca Almeida
- Felipe Melo
- Gabriel Belo
- Sophia Santos
- Iasmym Lorany

1. **Liderança de Produto (PO/PM):**
	- Visão estratégica, User Stories, coordenação de entregas e mediação técnica.

2. **Front-End:**
	- UX/UI Design no Figma, implementação da interface e integração com o fluxo de busca.

3. **Back-End & IA:**
	- Arquitetura de microsserviços, integração com APIs de IA (OpenRouter), processamento de Embeddings e Banco de Dados Vetorial.

---

## 📋 Funcionalidades do MVP (Etapa Atual)

- [ ] Interface de upload de fotos para busca e cadastro.
- [ ] Geração de descrição automática via IA (Nemotron).
- [ ] Persistência de dados (Foto + Descrição) no banco de dados.
- [ ] Filtro de busca por similaridade (Cosine Similarity > 0.7).
- [ ] Exibição de cards de sugestão baseados no "Match Score".

---

## 📄 Documentação Adicional

- [Guia de Contribuição (CONTRIBUTING.md)](CONTRIBUTING.md) - Padrões de código e branches.