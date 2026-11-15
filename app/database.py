import os
import sqlite3

from flask import current_app, g

SCHEMA = """
CREATE TABLE IF NOT EXISTS tutor (
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT NOT NULL,
    telefone  TEXT NOT NULL,
    email     TEXT NOT NULL DEFAULT ''
);

CREATE TABLE IF NOT EXISTS animal (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    tutor_id    INTEGER NOT NULL REFERENCES tutor (id) ON DELETE RESTRICT,
    nome        TEXT NOT NULL,
    especie     TEXT NOT NULL,
    raca        TEXT NOT NULL DEFAULT '',
    idade_anos  INTEGER
);
"""


def obter_conexao():
    if "db" not in g:
        conexao = sqlite3.connect(current_app.config["DATABASE_PATH"])
        conexao.row_factory = sqlite3.Row
        conexao.execute("PRAGMA foreign_keys = ON")
        g.db = conexao
    return g.db


def fechar_conexao(_erro=None):
    conexao = g.pop("db", None)
    if conexao is not None:
        conexao.close()


def inicializar_banco():
    caminho = current_app.config["DATABASE_PATH"]
    os.makedirs(os.path.dirname(os.path.abspath(caminho)), exist_ok=True)
    conexao = obter_conexao()
    conexao.executescript(SCHEMA)
    conexao.commit()


def linha_para_dict(linha):
    return dict(linha) if linha is not None else None
