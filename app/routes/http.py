from flask import request

SEM_CONTEUDO = ("", 204)


def corpo_json():
    return request.get_json(silent=True) or {}
