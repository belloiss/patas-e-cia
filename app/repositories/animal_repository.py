from sqlalchemy import delete, insert, select, update

from app.database import animal, buscar_um, buscar_varios, executar_e_confirmar


def listar_do_tutor(tutor_id):
    return buscar_varios(select(animal).where(animal.c.tutor_id == tutor_id).order_by(animal.c.nome))


def buscar(animal_id):
    return buscar_um(select(animal).where(animal.c.id == animal_id))


def criar(tutor_id, dados):
    resultado = executar_e_confirmar(insert(animal).values(**dados, tutor_id=tutor_id))
    return resultado.inserted_primary_key[0]


def atualizar(animal_id, dados):
    executar_e_confirmar(update(animal).where(animal.c.id == animal_id).values(**dados))


def excluir(animal_id):
    executar_e_confirmar(delete(animal).where(animal.c.id == animal_id))
