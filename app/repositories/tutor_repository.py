from app.database import linha_para_dict, obter_conexao

_SELECT_COM_TOTAL = """
    SELECT t.*, (SELECT COUNT(*) FROM animal a WHERE a.tutor_id = t.id) AS total_animais
    FROM tutor t
"""


def listar():
    linhas = obter_conexao().execute(_SELECT_COM_TOTAL + " ORDER BY t.nome").fetchall()
    return [dict(linha) for linha in linhas]


def buscar(tutor_id):
    linha = obter_conexao().execute(_SELECT_COM_TOTAL + " WHERE t.id = ?", (tutor_id,)).fetchone()
    return linha_para_dict(linha)


def criar(dados):
    conexao = obter_conexao()
    cursor = conexao.execute(
        "INSERT INTO tutor (nome, telefone, email) VALUES (:nome, :telefone, :email)", dados
    )
    conexao.commit()
    return cursor.lastrowid


def atualizar(tutor_id, dados):
    conexao = obter_conexao()
    conexao.execute(
        "UPDATE tutor SET nome = :nome, telefone = :telefone, email = :email WHERE id = :id",
        {**dados, "id": tutor_id},
    )
    conexao.commit()


def excluir(tutor_id):
    conexao = obter_conexao()
    conexao.execute("DELETE FROM tutor WHERE id = ?", (tutor_id,))
    conexao.commit()
