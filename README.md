# Achou Meu Pet AI?

Plataforma para encontrar pets perdidos usando visão computacional e busca vetorial.
**Stack:** Python + Flask (backend) | HTML / CSS / JS puro (frontend)

---

## Estrutura do projeto

```
meupet/
├── backend/
│   ├── app.py                        # Entry point Flask
│   ├── requirements.txt
│   ├── .env.example
│   ├── routes/
│   │   ├── pets.py                   # POST /api/pets/search, /register, /analyze
│   │   └── auth.py                   # POST /api/auth/register, /login
│   └── services/
│       ├── ai_service.py             # Visão + embedding via OpenRouter
│       └── supabase_service.py       # Upload, banco e auth via Supabase
└── frontend/
    ├── index.html                    # Todas as telas (SPA)
    ├── css/
    │   └── style.css
    └── js/
        └── app.js
```

---

## Instalação e execução

```bash
# 1. Entre na pasta do backend
cd backend

# 2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure as variáveis de ambiente
copy .env.example .env
# Edite o .env com suas chaves

# 5. Suba o servidor
python app.py
```

Acesse `http://localhost:5000` no navegador.

---

## Variáveis de ambiente (.env)

```
SUPABASE_URL=https://SEU_PROJETO.supabase.co
SUPABASE_ANON_KEY=sua_anon_key
OPENROUTER_API_KEY=sua_openrouter_key
```

---

## Endpoints da API

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/pets/search` | Busca pets por imagem ou descrição |
| POST | `/api/pets/register` | Cadastra pet encontrado (multipart) |
| POST | `/api/pets/analyze` | Analisa imagem com IA |
| POST | `/api/auth/register` | Cria conta de usuário |
| POST | `/api/auth/login` | Autentica usuário |

---

## Configuração do Supabase

1. Crie um projeto em supabase.com
2. Crie a tabela `pets` com as colunas: `species`, `breed`, `color`, `description`, `lastLocation`, `contactInfo`, `imageUrl`, `embedding` (vector)
3. Crie um bucket público chamado `pet_images`
4. Habilite a extensão `pgvector` e crie a função RPC `match_pets`
