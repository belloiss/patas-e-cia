from flask import Blueprint, jsonify

from app.routes.http import SEM_CONTEUDO, corpo_json
from app.services import tutor_service

bp = Blueprint("tutores", __name__, url_prefix="/api/tutores")


@bp.get("")
def listar():
    return jsonify(tutor_service.listar())


@bp.post("")
def criar():
    return jsonify(tutor_service.criar(corpo_json())), 201


@bp.get("/<int:tutor_id>")
def obter(tutor_id):
    return jsonify(tutor_service.obter(tutor_id))


@bp.put("/<int:tutor_id>")
def atualizar(tutor_id):
    return jsonify(tutor_service.atualizar(tutor_id, corpo_json()))


@bp.delete("/<int:tutor_id>")
def excluir(tutor_id):
    tutor_service.excluir(tutor_id)
    return SEM_CONTEUDO
