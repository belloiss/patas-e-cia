# Patas & Cia: cadastro de tutores e animais

Aplicação web da disciplina N695 (Desenvolvimento de Plataformas Web), Cenário 1: Clínica veterinária de bairro.

## O que faz

- Cadastra, lista, edita e exclui **tutores** e **animais** (um tutor tem vários animais).
- Valida campos obrigatórios, telefone brasileiro (DDD + 8 ou 9 dígitos), e-mail e idade.
- Impede excluir um tutor que ainda tenha animais cadastrados.

## Stack

- Interface: HTML, CSS e JavaScript puro (pasta `static/`), consumindo a API por `fetch`.
- Serviço Web: Python 3 + Flask (API REST em `/api`).
- Persistência: SQLite (banco de dados relacional com chave estrangeira entre `animal` e `tutor`).
- Hospedagem sugerida: Render (plano gratuito).

## Estrutura em camadas

```
app/
  routes/         interface HTTP (recebe a requisição e devolve JSON)
  services/       regras de negócio (ex.: bloqueio de exclusão)
  repositories/   acesso ao banco (SQL)
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

## Publicar no Render

1. Suba o projeto para um repositório **público** no GitHub.
2. No Render, crie um **Web Service** a partir do repositório.
3. Build command: `pip install -r requirements.txt`
4. Start command: `gunicorn wsgi:app`
5. Teste o link gerado e confirme que abre sem login.

Observação: no plano gratuito o disco é temporário, então o banco SQLite volta ao vazio quando o serviço reinicia ou é republicado. Cadastre alguns dados de exemplo antes de tirar as capturas de tela e antes da correção. Para dados permanentes, é possível trocar o SQLite por um PostgreSQL gratuito mexendo apenas na camada `repositories/`.

## Uso de IA generativa

Este projeto foi desenvolvido com apoio do Claude (Anthropic) para gerar a estrutura inicial do código e dos testes. A equipe revisou, executou e é capaz de explicar todo o código.
