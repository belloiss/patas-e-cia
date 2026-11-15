import os

from flask import Flask, jsonify
from werkzeug.exceptions import HTTPException

from app import database
from app.errors import AppError
from app.routes import animais, tutores

MENSAGENS_HTTP = {
    400: "Requisição inválida.",
    404: "Endereço não encontrado. Verifique o link e tente novamente.",
    405: "Operação não permitida neste endereço.",
}


def create_app(config=None):
    app = Flask(__name__, static_folder="../static", static_url_path="")
    app.config["DATABASE_URL"] = os.environ.get("DATABASE_URL")
    app.config.update(config or {})
    if not app.config["DATABASE_URL"]:
        app.config["DATABASE_URL"] = database.url_padrao(app)

    database.inicializar_banco(app)
    app.teardown_appcontext(database.fechar_conexao)
    app.register_blueprint(tutores.bp)
    app.register_blueprint(animais.bp)
    _registrar_tratadores_de_erro(app)

    @app.get("/")
    def pagina_inicial():
        return app.send_static_file("index.html")

    return app


def _registrar_tratadores_de_erro(app):
    @app.errorhandler(AppError)
    def tratar_erro_de_negocio(erro):
        return jsonify({"erro": erro.mensagem, "campos": erro.campos}), erro.status_code

    @app.errorhandler(Exception)
    def tratar_erro_inesperado(erro):
        if isinstance(erro, HTTPException):
            mensagem = MENSAGENS_HTTP.get(erro.code, "Não foi possível concluir a requisição.")
            return jsonify({"erro": mensagem, "campos": {}}), erro.code
        app.logger.exception(erro)
        return jsonify({"erro": "Erro interno. Tente novamente em instantes.", "campos": {}}), 500
