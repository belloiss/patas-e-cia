import re

from app.errors import ValidationError

ESPECIES = ("Cão", "Gato", "Ave", "Roedor", "Réptil", "Outro")
IDADE_MAXIMA = 40

_EMAIL = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def _texto(dados, campo):
    valor = dados.get(campo)
    return valor.strip() if isinstance(valor, str) else ""


def _apenas_digitos(texto):
    return re.sub(r"\D", "", texto)


def _telefone_valido(digitos):
    if len(digitos) not in (10, 11):
        return False
    if int(digitos[:2]) < 11:
        return False
    return len(digitos) == 10 or digitos[2] == "9"


def _levantar_se_houver(erros):
    if erros:
        raise ValidationError("Corrija os campos destacados.", erros)


def validar_tutor(dados):
    erros = {}
    nome = _texto(dados, "nome")
    telefone = _apenas_digitos(_texto(dados, "telefone"))
    email = _texto(dados, "email")

    if len(nome) < 2:
        erros["nome"] = "Informe o nome do tutor (mínimo de 2 letras)."
    if not telefone:
        erros["telefone"] = "Informe o telefone."
    elif not _telefone_valido(telefone):
        erros["telefone"] = "Telefone inválido. Use DDD e número, como (85) 98888-7777."
    if email and not _EMAIL.match(email):
        erros["email"] = "E-mail inválido. Use o formato nome@exemplo.com."

    _levantar_se_houver(erros)
    return {"nome": nome, "telefone": telefone, "email": email}


def _validar_idade(valor, erros):
    if valor in (None, ""):
        return None
    try:
        idade = int(valor)
    except (TypeError, ValueError):
        erros["idade_anos"] = "A idade deve ser um número inteiro."
        return None
    if not 0 <= idade <= IDADE_MAXIMA:
        erros["idade_anos"] = f"A idade deve estar entre 0 e {IDADE_MAXIMA} anos."
        return None
    return idade


def validar_animal(dados):
    erros = {}
    nome = _texto(dados, "nome")
    especie = _texto(dados, "especie")
    raca = _texto(dados, "raca")

    if not nome:
        erros["nome"] = "Informe o nome do animal."
    if not especie:
        erros["especie"] = "Escolha a espécie."
    elif especie not in ESPECIES:
        erros["especie"] = "Espécie inválida. Escolha uma das opções da lista."
    idade = _validar_idade(dados.get("idade_anos"), erros)

    _levantar_se_houver(erros)
    return {"nome": nome, "especie": especie, "raca": raca, "idade_anos": idade}
