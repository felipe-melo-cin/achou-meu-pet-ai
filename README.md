# 🐾 Achou Meu Pet AI?

> **Transformando fotos em reencontros através de Inteligência Artificial Multimodal.**

O **Achou Meu Pet AI?** é uma plataforma centralizada para auxiliar na localização de animais perdidos. O projeto resolve a ineficiência das redes sociais tradicionais ao utilizar modelos de Visão Computacional para identificar características de animais e busca vetorial para encontrar "matchs" de similaridade entre pets perdidos e encontrados.

---
## 🔄 Momento Atual e Evolução da Arquitetura (Transição)

Inicialmente, o projeto foi concebido utilizando Python em sua totalidade (incluindo o framework Flet para o Front-end). Para garantir maior escalabilidade, manutenibilidade e seguir padrões de mercado, **pivotamos nossa stack**.

> Atualmente, o repositório contém nosso **MVP Técnico** construído em **React com TypeScript**. 

Nesta etapa, o Front-end se comunica diretamente com os serviços (Supabase e IA). Na nossa **próxima sprint**, esta estrutura evoluirá para uma arquitetura Client-Server padrão, onde introduziremos uma **API REST** dedicada (Back-end) para intermediar essas requisições, garantindo maior segurança e facilidade de deploy.

---

## 🚀 O Diferencial Tecnológico: Fluxo de IA

Diferente de fóruns comuns, nossa aplicação automatiza a descrição e a busca:

1. **Visão (Image-to-Text):** O modelo de IA Multimodal (Google Gemini) analisa a foto e gera uma descrição técnica e objetiva (espécie, cor, porte, marcas).
2. **Vetorização (Embedding):** Essa descrição é convertida em um vetor matemático (lista de números).
3. **Busca Vetorial (Match Score):** Comparamos o vetor do animal procurado com o banco de dados usando **Similaridade por Cosseno**.
4. **Limiar de 70%:** O sistema apenas sugere ao usuário animais que possuam mais de **70% de similaridade** visual e descritiva, filtrando ruídos e aumentando a precisão.

---
## 📂 Estrutura do Repositório (Molde MVP e Futuro) 

Atualmente, o repositório contém a estrutura do nosso MVP em React na raiz. Na próxima sprint, esta estrutura evoluirá para separar claramente o Front-end do novo Back-end (API REST). 
```md
/achou-meu-pet-ai
├── /src                       # Código-fonte do Front-end (MVP Atual)
│   ├── /components            # Telas e blocos visuais (ImageUpload, SearchScreen, etc.)
│   ├── /lib                   # Funções utilitárias (utils.ts)
│   ├── /services              # Integrações diretas atuais (models.ts, supabase.ts)
│   ├── App.tsx                # Ponto de entrada das rotas
│   ├── index.css              # Estilos globais
│   ├── main.tsx               # Renderização principal do React
│   └── types.ts               # Tipagens globais do TypeScript
│
├── /backend                   # (PRÓXIMA SPRINT) Futura API REST em TypeScript/Python
│
├── .env                       # Variáveis de ambiente
├── .gitignore                 # Arquivos e pastas ignorados pelo Git
├── index.html                 # Template HTML principal
├── metadata.json              # Metadados do projeto
├── package.json               # Dependências e scripts do Node (Front-end)
├── package-lock.json          # Árvore de dependências travada
├── README.md                  # Visão geral do projeto
├── tsconfig.json              # Configurações do compilador TypeScript
└── vite.config.ts             # Configurações do bundler Vite
```
---
## 🛠️ Instalação e Execução Local (Frontend MVP)

Siga os passos abaixo para rodar o ambiente de desenvolvimento do nosso MVP Técnico em React:
### 1. Pré-requisitos

- _Node.js_ (v18+)
- Chaves de API: _OpenRouter_ e _Supabase_.
### 2. Configuração de Variáveis de Ambiente

Navegue até a pasta `/frontend` (ou na raiz, dependendo de como você clonou) e renomeie o arquivo `.env.example` para `.env`, preenchendo com as suas credenciais:

```Bash
VITE_OPENROUTER_API_KEY=sua_chave_aqui
VITE_SUPABASE_URL=sua_url_supabase
VITE_SUPABASE_ANON_KEY=sua_chave_anon_public
```

### 3. Instalando dependências e Subindo a Aplicação

Abra o terminal no diretório do projeto front-end e execute:

```Bash
# Instala as dependências do projeto
npm install



# Inicia o servidor de desenvolvimento Vite
npm run dev
```

- **Frontend:** Disponível em http://localhost:3000/ (porta padrão do Vite)

---

## 👥 Equipe e Divisão de Papéis

O projeto é desenvolvido por uma equipe de 6 integrantes, com papéis rotativos para garantir o aprendizado em todas as frentes:

**Integrantes (Equipe Inicial):**

- Arthur Araújo
- Bianca Almeida
- Felipe Melo
- Gabriel Belo
- Sophia Santos
- Iasmym Lorany

1. **Liderança de Produto (PO/PM):** Visão estratégica, User Stories, coordenação de entregas e mediação técnica.

2. **Front-End:** UX/UI Design no Figma, implementação da interface React e integração.

3. **Back-End & IA:** Arquitetura da futura API REST, integração com APIs de IA, processamento de Embeddings e Banco de Dados (Dinâmico e Vetorial).

---

## 📄 Documentação Adicional

- [Guia de Contribuição (CONTRIBUTING.md)](https://www.google.com/search?q=CONTRIBUTING.md) - Padrões de código e branches.