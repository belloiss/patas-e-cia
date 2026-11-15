from flask import Blueprint, jsonify

from app.routes.http import SEM_CONTEUDO, corpo_json
from app.services import animal_service

bp = Blueprint("animais", __name__, url_prefix="/api")


@bp.get("/tutores/<int:tutor_id>/animais")
def listar_do_tutor(tutor_id):
    return jsonify(animal_service.listar_do_tutor(tutor_id))


@bp.post("/tutores/<int:tutor_id>/animais")
def criar(tutor_id):
    return jsonify(animal_service.criar(tutor_id, corpo_json())), 201


@bp.get("/animais/<int:animal_id>")
def obter(animal_id):
    return jsonify(animal_service.obter(animal_id))


@bp.put("/animais/<int:animal_id>")
def atualizar(animal_id):
    return jsonify(animal_service.atualizar(animal_id, corpo_json()))


@bp.delete("/animais/<int:animal_id>")
def excluir(animal_id):
    animal_service.excluir(animal_id)
    return SEM_CONTEUDO
