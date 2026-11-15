from sqlalchemy import delete, func, insert, select, update

from app.database import animal, buscar_um, buscar_varios, executar_e_confirmar, tutor

_total_animais = (
    select(func.count()).where(animal.c.tutor_id == tutor.c.id).scalar_subquery().label("total_animais")
)
_SELECT_COM_TOTAL = select(tutor, _total_animais)


def listar():
    return buscar_varios(_SELECT_COM_TOTAL.order_by(tutor.c.nome))


def buscar(tutor_id):
    return buscar_um(_SELECT_COM_TOTAL.where(tutor.c.id == tutor_id))


def criar(dados):
    resultado = executar_e_confirmar(insert(tutor).values(**dados))
    return resultado.inserted_primary_key[0]


def atualizar(tutor_id, dados):
    executar_e_confirmar(update(tutor).where(tutor.c.id == tutor_id).values(**dados))


def excluir(tutor_id):
    executar_e_confirmar(delete(tutor).where(tutor.c.id == tutor_id))
