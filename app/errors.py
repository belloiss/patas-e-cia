class AppError(Exception):
    """Erro de negócio que vira uma resposta HTTP com mensagem clara."""

    status_code = 500

    def __init__(self, mensagem, campos=None):
        super().__init__(mensagem)
        self.mensagem = mensagem
        self.campos = campos or {}


class ValidationError(AppError):
    status_code = 400


class NotFoundError(AppError):
    status_code = 404


class ConflictError(AppError):
    status_code = 409
