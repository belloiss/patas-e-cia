from app.errors import ConflictError, NotFoundError
from app.repositories import tutor_repository
from app.validators import validar_tutor


def obter_ou_falhar(tutor_id):
    tutor = tutor_repository.buscar(tutor_id)
    if tutor is None:
        raise NotFoundError("Tutor não encontrado.")
    return tutor


def listar():
    return tutor_repository.listar()


def obter(tutor_id):
    return obter_ou_falhar(tutor_id)


def criar(dados):
    tutor_id = tutor_repository.criar(validar_tutor(dados))
    return obter_ou_falhar(tutor_id)


def atualizar(tutor_id, dados):
    obter_ou_falhar(tutor_id)
    tutor_repository.atualizar(tutor_id, validar_tutor(dados))
    return obter_ou_falhar(tutor_id)


def excluir(tutor_id):
    tutor = obter_ou_falhar(tutor_id)
    total = tutor["total_animais"]
    if total > 0:
        animais = "1 animal cadastrado" if total == 1 else f"{total} animais cadastrados"
        raise ConflictError(
            f"Não é possível excluir {tutor['nome']}: o tutor ainda tem "
            f"{animais}. Exclua os animais primeiro."
        )
    tutor_repository.excluir(tutor_id)
