# 🐾 Achou Meu Pet AI?

> **Reconectando pets perdidos aos seus donos através de Inteligência Artificial.**

O **Achou Meu Pet AI?** é uma plataforma centralizada para auxiliar na localização de animais perdidos. O projeto resolve a ineficiência das redes sociais tradicionais ao utilizar **Visão Computacional** para descrever características de animais e **busca vetorial** (pgvector) para encontrar _matches_ de similaridade entre pets perdidos e encontrados.

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Arquitetura](#-arquitetura)
- [Fluxo de IA](#-fluxo-de-ia)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Pré-requisitos](#-pré-requisitos)
- [Configuração no Supabase](#-configuração-no-supabase)
- [Instalação e Execução Local](#-instalação-e-execução-local)
- [Endpoints da API](#-endpoints-da-api)
- [Testes](#-testes)
- [Deploy no Render](#-deploy-no-render)
- [Equipe](#-equipe)
- [Contribuindo](#-contribuindo)

---

## 🔍 Sobre o Projeto

Diferente de grupos em redes sociais onde anúncios se perdem no feed, o **Achou Meu Pet AI?** automatiza o processo de identificação e busca:

- Ao **reportar um pet encontrado**, o usuário faz upload de uma foto e a IA descreve automaticamente espécie, raça, cor e marcas do animal.
- Ao **procurar um pet perdido**, o sistema compara a foto enviada com todos os registros do banco via similaridade vetorial, retornando apenas os matches acima de **70%** de similaridade.
- Isso elimina a triagem manual e aumenta drasticamente a precisão das sugestões.

---

## 🏛 Arquitetura

O projeto utiliza uma arquitetura **Client-Server (MVC simplificado)**, com separação clara entre frontend e backend:
```
┌─────────────────────────────────────────────────────────────────┐
──────┐
│                         CLIENTE (Browser)                       │
│              HTML + CSS + JavaScript Vanilla (SPA)              │
│     index.html · partials.js · styles.css · (Mock API → Real)   │
└──────────────────────┬──────────────────────────────────────────┘
──────┘
│  HTTP (fetch / form-data)
▼
┌─────────────────────────────────────────────────────────────────┐
──────┐
│                   BACKEND — Flask (Python)                      │
│                                                                 │
│   app.py  ──► Blueprint /api/auth  ──► services/supabase.py     │
│           └──► Blueprint /api/pets  ──► services/ai_service.py  │
│                                    └──► services/supabase.py    │
└──────────────────────┬─────────────────────────┬───────────────┘
─────┘
│ │
┌───────────▼───────────┐  ┌──────────▼──────────────┐
│   Supabase (BaaS)     │  │   OpenRouter (AI API)   │
│  Auth · PostgreSQL    │  │  Vision Model (QianFan) │
│  pgvector · Storage   │  │  Embedding (text-3-sm)  │
└───────────────────────┘  └─────────────────────────┘
```

### Camadas da Arquitetura

**Frontend (cliente estático)**
Construído em HTML, CSS e JavaScript Vanilla, servido diretamente pelo Flask como arquivos estáticos. A navegação entre telas é feita via SPA (Single-Page Application) com troca de páginas por CSS (`display: none / flex`). Atualmente usa um **Mock API** (`partials.js`) que deve ser substituído por chamadas `fetch` reais à API do backend.

**Backend (API REST — Flask)**
Organizado em Blueprints e camadas de serviço:
- `routes/` — Controllers HTTP (recebem request, delegam para services, devolvem JSON)
- `services/` — Lógica de negócio isolada (chamadas à IA, operações no Supabase)
- `models/` — Reservado para modelos de dados / DTOs (expansão futura)

**Supabase (BaaS)**
Provê três recursos: autenticação (Supabase Auth), banco de dados relacional com extensão `pgvector` (tabela `pets` com coluna `embedding`), e armazenamento de imagens (bucket `pet_images`).

**OpenRouter**
Gateway de IA usado para duas chamadas distintas: análise de imagem via modelo multimodal (visão) e geração de embeddings textuais.

### Por que essa arquitetura?

A separação entre frontend e backend permite que o cliente seja hospedado em qualquer CDN (Netlify, Vercel) enquanto o servidor roda em qualquer plataforma Python (Railway, Render, Fly.io). As chaves de API ficam **apenas no servidor**, nunca expostas ao browser — diferente do MVP anterior em React que as expunha via variáveis `VITE_*`.

---

## 🚀 Fluxo de IA
```
Foto do pet (base64)
│
▼
┌─────────────────────┐
│  Vision Analysis    │  ← Modelo multimodal (nex-n2-pro / OpenRouter)
│  (pet_vision_       │    Retorna JSON: { species, breed,
│   analysis)         │      primaryColor, distinguishingMarks }
└────────┬────────────┘
│  texto concatenado
▼
┌─────────────────────┐
│  Embedding          │  ← nvidia/llama-nemotron-embed-vl-1b-v2:free
│  (generate_         │    Retorna vetor float[] de 1024 dimensões
│   embedding)        │
└────────┬────────────┘
│  vetor
▼
┌─────────────────────┐
│  pgvector (RPC      │  ← match_pets() — Similaridade por Cosseno
│  match_pets)        │    Filtra threshold ≥ 0.5 (busca) / 0.7 (UI)
└─────────────────────┘
```

---

## 📂 Estrutura do Repositório

```
achou-meu-pet-ai/
├── backend/
│   ├── app.py                  # Entry point Flask, blueprints, rota /api/health
│   ├── requirements.txt        # Dependências Python
│   ├── .env.example            # Template de variáveis de ambiente
│   
│   ├── routes/
│   │   ├── init.py
│   │   ├── auth.py             # POST /api/auth/register, POST /api/auth/login
│   │   └── pets.py             # GET /api/pets, POST /api/pets/search,
│   │                           # POST /api/pets/register, POST /api/pets/analyze
│   └── services/
│       ├── init.py
│       ├── ai_service.py       # pet_vision_analysis(), generate_embedding()
│       └── supabase_service.py # upload_image(), register_pet(), list_pets(),
│                               # search_similar_pets(), register_user(), login_user()
│
└── frontend/
├── index.html              # SPA principal (todas as telas em uma página)
├── css/
│   └── styles.css          # Estilos globais
└── js/
└── partials.js         # Navbar, footer, SVGs e Mock API
```

---

## ✅ Pré-requisitos

- **Python 3.11+**
- **pip**
- Conta no **Supabase** (gratuita) com:
  - Extensão `pgvector` habilitada
  - Tabela `pets` com colunas: `id, species, breed, color, description, lastLocation, contactInfo, imageUrl, embedding (vector), created_at`
  - Função RPC `match_pets` criada (ver seção de Configuração no Supabase)
  - Bucket de storage `pet_images` (público)
- Chave de API do **OpenRouter** (gratuita para modelos free)

---

## 🛠 Configuração no Supabase

Para que o backend funcione perfeitamente, você precisará configurar 4 pilares no seu painel do Supabase:

### 1. Habilitar a Extensão de Vetores

No SQL Editor do Supabase, execute o comando abaixo para habilitar a extensão responsável por buscas vetoriais:

```sql
create extension if not exists vector;
```

### 2. Criar a Tabela `pets`

A tabela precisa acomodar os metadados do pet e a coluna de embedding para armazenar o vetor gerado pelo modelo da NVIDIA. O modelo `llama-nemotron-embed-vl-1b-v2` gera vetores de **1024 dimensões**:

```sql
create table pets (
  id uuid default gen_random_uuid() primary key,
  species text default 'Desconhecido',
  breed text,
  color text,
  description text,
  "lastLocation" text not null,
  "contactInfo" text,
  "imageUrl" text,
  embedding vector(1024),
  created_at timestamp with time zone default timezone('utc'::text, now()) not null
);
```

### 3. Criar a Função RPC `match_pets`

O backend executa uma chamada RPC para calcular a distância de cosseno entre vetores. Execute o script abaixo no Supabase SQL Editor:

```sql
create or replace function match_pets (
  query_embedding vector(1024),
  match_threshold float,
  match_count int
)
returns table (
  id uuid,
  species text,
  breed text,
  color text,
  description text,
  "lastLocation" text,
  "contactInfo" text,
  "imageUrl" text,
  created_at timestamp with time zone
)
language plpgsql as $$
begin
  return query
  select
    pets.id,
    pets.species,
    pets.breed,
    pets.color,
    pets.description,
    pets."lastLocation",
    pets."contactInfo",
    pets."imageUrl",
    pets.created_at
  from pets
  where 1 - (pets.embedding <=> query_embedding) > match_threshold
  order by pets.embedding <=> query_embedding asc
  limit match_count;
end;
$$;
```

### 4. Criar o Bucket de Storage `pet_images`

1. Acesse **Storage** no menu lateral do Supabase.
2. Crie um novo bucket chamado **`pet_images`**.
3. Altere a visibilidade do bucket para **Public** (para que as URLs públicas funcionem sem restrições de assinatura).
4. Adicione políticas de segurança (RLS) que permitam inserção de arquivos de forma anônima ou autenticada conforme sua regra de negócio.

---

## 🛠 Instalação e Execução Local

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/achou-meu-pet-ai.git
cd achou-meu-pet-ai
```

### 2. Crie e ative um ambiente virtual

```bash
# Linux / macOS
python3 -m venv .venv
source .venv/bin/activate

# Windows (PowerShell)
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Instale as dependências

```bash
cd backend
pip install -r requirements.txt
```

Dependências instaladas:

| Pacote | Versão | Uso |
|---|---|---|
| `flask` | 3.1.0 | Framework web |
| `flask-cors` | 5.0.0 | Habilitar CORS para o frontend |
| `python-dotenv` | 1.0.1 | Carregar variáveis de ambiente |
| `supabase` | 2.10.0 | Client Supabase (auth, db, storage) |
| `openai` | 1.51.0 | Client OpenAI-compatible (OpenRouter) |

### 4. Configure as variáveis de ambiente

Dentro da pasta `backend/`, copie o arquivo de exemplo e preencha com suas credenciais:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:

```env
SUPABASE_URL=https://SEU_PROJETO.supabase.co
SUPABASE_ANON_KEY=sua_anon_key_aqui
OPENROUTER_API_KEY=sua_openrouter_key_aqui
```

> **Onde encontrar cada chave:**
> - `SUPABASE_URL` e `SUPABASE_ANON_KEY`: Painel Supabase → Settings → API
> - `OPENROUTER_API_KEY`: [openrouter.ai/keys](https://openrouter.ai/keys)

### 5. Suba o servidor

```bash
# Ainda dentro de backend/
python app.py
```

O servidor inicia em **http://localhost:5000**.

Acesse **http://localhost:5000** no browser para ver o frontend. Verifique a saúde da API em **http://localhost:5000/api/health** — deve retornar `{"status": "ok"}`.

---

## 📡 Endpoints da API

### Auth

| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/auth/register` | Cria novo usuário |
| `POST` | `/api/auth/login` | Autentica e retorna token |

**Exemplo — Cadastro:**
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"joao@email.com","senha":"123456","nome":"João","sobrenome":"Silva"}'
```

**Exemplo — Login:**
```bash
curl -X POST http://localhost:5000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"joao@email.com","senha":"123456"}'
```

### Pets

| Método | Rota | Descrição |
|---|---|---|
| `GET` | `/api/pets` | Lista os 50 pets mais recentes |
| `POST` | `/api/pets/register` | Cadastra um pet encontrado (multipart/form-data) |
| `POST` | `/api/pets/analyze` | Analisa foto e retorna descrição JSON |
| `POST` | `/api/pets/search` | Busca pets similares via embedding |

**Exemplo — Analisar imagem:**
```bash
# Converta a imagem para base64 antes
IMAGE_B64=$(base64 -w 0 foto_do_pet.jpg)

curl -X POST http://localhost:5000/api/pets/analyze \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_B64\"}"
```

**Exemplo — Buscar pet perdido:**
```bash
curl -X POST http://localhost:5000/api/pets/search \
  -H "Content-Type: application/json" \
  -d "{\"image\": \"$IMAGE_B64\"}"
```

**Exemplo — Registrar pet encontrado:**
```bash
curl -X POST http://localhost:5000/api/pets/register \
  -F "image=@foto_do_pet.jpg" \
  -F "raca=Golden Retriever" \
  -F "cor=Dourado" \
  -F "cidade=Recife - PE" \
  -F "descricao=Encontrado no Parque da Jaqueira, muito dócil." \
  -F "contato=(81) 99999-9999"
```

---

## 🧪 Testes

### Tipos e Técnicas

Os testes estão localizados em `backend/tests/` e cobrem duas categorias:

**Testes Unitários** — verificam funções e métodos isoladamente, sem dependências externas reais. São aplicados sobre as camadas de serviço (`ai_service`, `supabase_service`) e sobre as rotas HTTP.

**Testes de Integração (de rota)** — verificam o comportamento completo de cada endpoint HTTP usando o `test_client` do Flask, garantindo que request → validação → resposta funciona de ponta a ponta dentro da aplicação.

A técnica de geração usada em todos os testes é **Mock/Stub via `unittest.mock`**: as dependências externas (Supabase e OpenRouter) são substituídas por objetos falsos controlados, tornando os testes rápidos, determinísticos e executáveis sem nenhuma chave de API real.

| Arquivo | Tipo | O que cobre |
|---|---|---|
| `tests/test_ai_service.py` | Unitário | `pet_vision_analysis`, `generate_embedding` |
| `tests/test_supabase_service.py` | Unitário | `register_pet`, `list_pets`, `search_similar_pets`, `login_user` |
| `tests/test_routes.py` | Integração de rota | `/api/health`, `/api/pets/*`, `/api/auth/register` |

### Instalação das dependências de teste

```bash
cd backend
pip install pytest pytest-mock pytest-cov
```

### Como executar

```bash
# Todos os testes
pytest tests/ -v

# Um arquivo específico
pytest tests/test_ai_service.py -v

# Com relatório de cobertura
pytest tests/ --cov=. --cov-report=term-missing
```

Saída esperada ao rodar tudo:
```bash
tests/test_ai_service.py::TestPetVisionAnalysis::test_retorna_dict_com_campos_esperados PASSED

tests/test_ai_service.py::TestPetVisionAnalysis::test_limpa_markdown_do_json PASSED

tests/test_ai_service.py::TestPetVisionAnalysis::test_levanta_erro_quando_conteudo_vazio PASSED

...

====== 16 passed in 1.23s ======
```

---

## 🚀 Deploy no Render

O Render é ideal para hospedar essa aplicação Flask de forma rápida e gratuita. Siga o passo a passo abaixo:

### Passo 1: Preparar o Repositório

Certifique-se de incluir um arquivo `requirements.txt` na raiz do projeto contendo todas as dependências:

```
Flask==3.1.0
flask-cors==5.0.0
python-dotenv==1.0.1
supabase==2.10.0
openai==1.51.0
gunicorn==21.2.0
```

### Passo 2: Criar um Web Service no Render

1. Acesse o dashboard do [Render](https://render.com) e clique em **New +** > **Web Service**.
2. Conecte o repositório do GitHub onde o código do projeto está hospedado.
3. Defina as configurações básicas do ambiente:
   - **Language:** `Python`
   - **Region:** Escolha a mais próxima do seu banco Supabase (geralmente _Ohio (us-east-2)_ ou _Frankfurt (eu-central-1)_).
   - **Branch:** `main` (ou a branch de produção de sua preferência).

### Passo 3: Comandos de Inicialização

Preencha os campos de compilação da seguinte forma:

- **Build Command:**
```bash
  pip install -r requirements.txt
```

- **Start Command:** (Usando gunicorn para produção em vez do servidor de desenvolvimento do Flask)
```bash
  gunicorn app:app
```

### Passo 4: Variáveis de Ambiente

No menu lateral da configuração do serviço no Render, clique em **Environment** e adicione as seguintes chaves:

| Chave | Descrição / Valor |
|---|---|
| `SUPABASE_URL` | URL do seu projeto Supabase (encontrada em Project Settings > API) |
| `SUPABASE_ANON_KEY` | Chave pública anônima do seu projeto Supabase |
| `OPENROUTER_API_KEY` | Sua chave de API gerada no painel do OpenRouter |

> ⚠️ **Nota:** A aplicação automaticamente ouvirá na porta fornecida de forma dinâmica pelo Render através da variável de ambiente `$PORT`, o que faz o `gunicorn` se adaptar nativamente sem precisar fixar a porta `5000` em produção.

### Passo 5: Deploy Automático

Após salvar as configurações, o Render iniciará automaticamente o deploy. Você pode acompanhar o progresso na aba **Logs**. Uma vez concluído, sua aplicação estará disponível em um URL público (ex: `https://achou-meu-pet-ai.onrender.com`).

---

## 👥 Equipe

O projeto é desenvolvido por uma equipe de 6 integrantes com papéis rotativos:

| Integrante | Papel Principal |
|---|---|
| Arthur Araújo | Liderança de Produto (PO/PM) |
| Bianca Almeida | Front-End / UX |
| Felipe Melo | Back-End & IA |
| Gabriel Belo | Back-End & IA |
| Pedro Henrique | Front-End / UX |
| Iasmym Lorany | Liderança de Produto (PO/PM) |

---

## 🤝 Contribuindo

Quer contribuir com o projeto? Leia o [CONTRIBUTING.md](CONTRIBUTING.md) para entender os padrões de código, convenção de branches e o fluxo de pull request adotado pela equipe.

---

## 📄 Licença

Este projeto está sob a licença MIT. Consulte o arquivo `LICENSE` para mais detalhes.