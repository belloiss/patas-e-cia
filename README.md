# Patas & Cia: cadastro de tutores e animais

Aplicação web da disciplina N695 (Desenvolvimento de Plataformas Web), Cenário 1: Clínica veterinária de bairro.

- **Aplicação publicada:** https://patas-e-cia-d5ve.onrender.com
- **Repositório:** https://github.com/belloiss/patas-e-cia

## O que faz

- Cadastra, lista, edita e exclui **tutores** e **animais** (um tutor tem vários animais).
- Valida campos obrigatórios, telefone brasileiro (DDD + 8 ou 9 dígitos), e-mail e idade.
- Impede excluir um tutor que ainda tenha animais cadastrados.

## Stack

- Interface: HTML, CSS e JavaScript puro (pasta `static/`), consumindo a API por `fetch`.
- Serviço Web: Python 3 + Flask (API REST em `/api`).
- Persistência: PostgreSQL (banco de dados relacional com chave estrangeira entre `animal` e `tutor`), acessado com SQLAlchemy Core.
  Sem a variável `DATABASE_URL`, a aplicação usa um arquivo SQLite local (útil para desenvolver e para os testes); o código é o mesmo.
- Hospedagem: Render (aplicação) + Neon (PostgreSQL), ambos no plano gratuito.

## Estrutura em camadas

```
app/
  routes/         interface HTTP (recebe a requisição e devolve JSON)
  services/       regras de negócio (ex.: bloqueio de exclusão)
  repositories/   consultas ao banco
  database.py     tabelas, conexão e execução de comandos
  validators.py   validação de entrada
  errors.py       erros de negócio -> respostas HTTP claras
static/           telas HTML, CSS e JS
tests/            testes automatizados da API
```

## Endpoints

| Método | Rota | Ação |
|---|---|---|
| GET | `/api/tutores` | Lista tutores |
| POST | `/api/tutores` | Cria tutor |
| GET / PUT / DELETE | `/api/tutores/<id>` | Consulta, atualiza, exclui tutor |
| GET | `/api/tutores/<id>/animais` | Lista animais do tutor |
| POST | `/api/tutores/<id>/animais` | Cria animal |
| GET / PUT / DELETE | `/api/animais/<id>` | Consulta, atualiza, exclui animal |

Erros retornam `{"erro": "mensagem", "campos": {"campo": "mensagem"}}` com status 400, 404 ou 409.

## Rodar localmente

```
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python -m flask --app wsgi run
```

Acesse http://127.0.0.1:5000. Para os testes: `python -m unittest discover -s tests -v`.

Para rodar localmente usando PostgreSQL, defina a variável antes de iniciar:
`DATABASE_URL=postgresql://usuario:senha@host/banco` (no PowerShell: `$env:DATABASE_URL="..."`).

## Publicar (Neon + Render)

1. Suba o projeto para um repositório **público** no GitHub.
2. Em [neon.tech](https://neon.tech), crie um projeto gratuito e copie a *connection string*
   (começa com `postgresql://` e termina com `?sslmode=require`).
3. No Render, crie um **Web Service** a partir do repositório:
   - Build command: `pip install -r requirements.txt`
   - Start command: `gunicorn wsgi:app`
   - Em *Environment*, adicione a variável `DATABASE_URL` com a connection string do Neon.
4. As tabelas são criadas automaticamente na primeira execução.
5. Teste o link gerado numa aba anônima e confirme que abre sem login.

Os dados ficam no Neon, então não se perdem quando o Render reinicia ou republica o serviço.
No plano gratuito, o Render "dorme" após 15 minutos sem acesso; o primeiro acesso depois disso pode levar cerca de 1 minuto.

## Uso de IA generativa

Este projeto foi desenvolvido com apoio do Claude (Anthropic) para gerar a estrutura inicial do código e dos testes. A equipe revisou, executou e é capaz de explicar todo o código.
