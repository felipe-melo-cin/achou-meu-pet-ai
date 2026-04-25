Bem-vindo ao repositório oficial do projeto! Este documento define as regras de colaboração para a nossa equipe de 6 integrantes.
## 👥 Divisão da Equipe

- **PO/PM (1 integrante):** Responsável por definir as **User Stories**, validar o progresso das Sprints, coordenar as atividades entre as áreas e garantir que o produto final atenda à visão original. 
  > É o "voto de minerva" em decisões de produto.

- **Front-End (2 integrantes):** Foco na interface de busca, anexação de fotos e exibição de matches (Baseado no protótipo do vídeo).]

- **Back-End (3 integrantes):** Foco na pipeline de IA, gerenciamento do banco de dados vetorial e integração com APIs externas.

## 🛠 Stack Tecnológica

- **IA Vision:** OpenRouter (NVIDIA Nemotron-70B-Instruct). -  *Fase de Testes*
- **IA Embedding:** OpenRouter (NVIDIA Llama Nemotron Embed VL 1B). - *Fase de Testes*
- **Banco de Dados:** Supabase (PostgreSQL + pgvector).
- **Front-End:** React.js / Next.js.
- **Back-End:** Python (FastAPI).

## 1. Comunicação e Gestão de Tarefas

- **Discussões Técnicas:** 
	- Centralizadas no **Discord** (Dailies e Reuniões de planejamento). 
	- Decisões rápidas de coordenação via **WhatsApp**.

- **Gestão de Tarefas:** Utilizamos o **Notion** para o Backlog e acompanhamento das Sprints.

- **Atribuição:** Ninguém deve iniciar uma funcionalidade sem que a tarefa esteja movida para "Em andamento" e atribuída ao seu perfil no board, ou sequer exista no board.

## 2. Padrão de Nomenclatura de Branches

Nossa branch principal de produção é a `main`. O desenvolvimento ocorre na branch `develop`. Cada branch a partir da develop segue o padrão:

| Tipo                          | Prefixo    | Exemplo                       |
| ----------------------------- | ---------- | ----------------------------- |
| **Nova Funcionalidade Front** | `feat/fe-` | `feat/fe-map-display`         |
| **Nova Funcionalidade Back**  | `feat/be-` | `feat/be-supabase-crud`       |
| **Lógica de IA / Prompts**    | `feat/ai-` | `feat/ai-nemotron-prompt`     |
| **Correção de Bug Front**     | `fix/fe-`  | `fix/fe-button-alignment`     |
| **Correção de Bug Back**      | `fix/be-`  | `fix/be-database-timeout`     |
| **Ajuste na IA / Embedding**  | `fix/ai-`  | `fix/ai-prompt-hallucination` |

## 3. Padrão de Commits

Utilizamos o padrão **Conventional Commits**. A mensagem deve ser em português:

- `feat`: Nova funcionalidade (Ex: `feat: implementa busca por similaridade de cosseno`)

- `fix`: Correção de bug (Ex: `fix: corrige erro no upload de arquivos grandes`)

- `docs`:Alterações documentação (Ex: `docs: adiciona guia de configuração da API`)

- `Style`: Melhoria no código sem alterar comportamento (Ex: `refactor: otimiza chamada da API de embedding`)

- `ai`: Mudanças específicas em prompts ou modelos (Ex: `ai: ajusta prompt do nemotron para maior objetividade`)

## 4. Fluxo de Trabalho e Pull Requests (PRs)

1. Certifique-se de que sua branch está atualizada com a `develop`.
	- Utilize o `git fetch origin` para verificar as atualizações.
	- Após isso verifique com `git status` para descobrir se a branch está atrasada.
	- Caso esteja, atualize usando `git pull origin develop`.

2. Após finalizar suas alterações e realizar o commit seguindo os padrões, abra um **Pull Request** para a branch `develop`.

3. **Revisão Obrigatória:** O PR deve ser aprovado por pelo menos **1 membro da equipe oposta** (se você é Front, um Back revisa; se é Back, um Front ou outro Back revisa) e pelo PM/PO verificando a resposta para a *user story*.
> Isso garante que todos entendam o fluxo completo.

## 5. Padrões de Código e UI

- **Idioma:** O código (variáveis, funções, classes) deve ser escrito em **Inglês**. Comentários e documentação em **Português**.
    
- **Front-End (2 devs):** Deve seguir fielmente o protótipo (vídeo anexo):
    
    - Cores: Branco, Cinza claro e Verde destaque.
    - Feedback visual: Exibir "Obrigado por contribuir" após o cadastro.
    - Cards: Mostrar local (Cidade/UF) e tempo de postagem abaixo da imagem do pet.
    
- **Back-End (3 devs):**
    
    - Utilizar variáveis de ambiente (.env) para as chaves da API (OpenRouter, Supabase). Nunca suba chaves para o repositório.
    - Implementar tratamento de erro para quando a IA falhar em descrever a imagem.