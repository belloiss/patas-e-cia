from app.errors import NotFoundError
from app.repositories import animal_repository
from app.services import tutor_service
from app.validators import validar_animal


def _obter_ou_falhar(animal_id):
    animal = animal_repository.buscar(animal_id)
    if animal is None:
        raise NotFoundError("Animal não encontrado.")
    return animal


def listar_do_tutor(tutor_id):
    tutor_service.obter_ou_falhar(tutor_id)
    return animal_repository.listar_do_tutor(tutor_id)


def obter(animal_id):
    return _obter_ou_falhar(animal_id)


def criar(tutor_id, dados):
    tutor_service.obter_ou_falhar(tutor_id)
    animal_id = animal_repository.criar(tutor_id, validar_animal(dados))
    return _obter_ou_falhar(animal_id)


def atualizar(animal_id, dados):
    _obter_ou_falhar(animal_id)
    animal_repository.atualizar(animal_id, validar_animal(dados))
    return _obter_ou_falhar(animal_id)


def excluir(animal_id):
    _obter_ou_falhar(animal_id)
    animal_repository.excluir(animal_id)
