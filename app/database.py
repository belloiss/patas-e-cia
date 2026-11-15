"""Camada de dados: tabelas, conexão e execução de comandos no banco.

Em produção usa PostgreSQL (variável de ambiente DATABASE_URL).
Sem DATABASE_URL, usa um arquivo SQLite local, útil para desenvolver e testar.
"""

import os

from flask import current_app, g
from sqlalchemy import Column, ForeignKey, Integer, MetaData, String, Table, create_engine, event

CHAVE_DO_MOTOR = "motor_do_banco"

metadata = MetaData()

tutor = Table(
    "tutor",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("nome", String(120), nullable=False),
    Column("telefone", String(11), nullable=False),
    Column("email", String(254), nullable=False, server_default=""),
)

animal = Table(
    "animal",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("tutor_id", Integer, ForeignKey("tutor.id", ondelete="RESTRICT"), nullable=False, index=True),
    Column("nome", String(120), nullable=False),
    Column("especie", String(20), nullable=False),
    Column("raca", String(80), nullable=False, server_default=""),
    Column("idade_anos", Integer),
)


def url_padrao(app):
    os.makedirs(app.instance_path, exist_ok=True)
    return "sqlite:///" + os.path.join(app.instance_path, "clinica.db")


def _normalizar_url(url):
    """Render e Neon entregam 'postgres://' ou 'postgresql://'; o SQLAlchemy precisa saber o driver."""
    for prefixo in ("postgres://", "postgresql://"):
        if url.startswith(prefixo):
            return "postgresql+psycopg://" + url[len(prefixo):]
    return url


def _ativar_chaves_estrangeiras_no_sqlite(motor):
    @event.listens_for(motor, "connect")
    def ativar(conexao_dbapi, _registro):
        conexao_dbapi.execute("PRAGMA foreign_keys = ON")


def inicializar_banco(app):
    url = _normalizar_url(app.config["DATABASE_URL"])
    motor = create_engine(url, pool_pre_ping=True)
    if motor.dialect.name == "sqlite":
        _ativar_chaves_estrangeiras_no_sqlite(motor)
    metadata.create_all(motor)
    app.extensions[CHAVE_DO_MOTOR] = motor


def encerrar_banco(app):
    app.extensions.pop(CHAVE_DO_MOTOR).dispose()


def obter_conexao():
    if "db" not in g:
        g.db = current_app.extensions[CHAVE_DO_MOTOR].connect()
    return g.db


def fechar_conexao(_erro=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def buscar_varios(consulta):
    return [dict(linha) for linha in obter_conexao().execute(consulta).mappings()]


def buscar_um(consulta):
    linha = obter_conexao().execute(consulta).mappings().first()
    return dict(linha) if linha is not None else None


def executar_e_confirmar(comando):
    conexao = obter_conexao()
    resultado = conexao.execute(comando)
    conexao.commit()
    return resultado
