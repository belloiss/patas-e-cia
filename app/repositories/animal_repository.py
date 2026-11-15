from app.database import linha_para_dict, obter_conexao


def listar_do_tutor(tutor_id):
    linhas = obter_conexao().execute(
        "SELECT * FROM animal WHERE tutor_id = ? ORDER BY nome", (tutor_id,)
    ).fetchall()
    return [dict(linha) for linha in linhas]


def buscar(animal_id):
    linha = obter_conexao().execute("SELECT * FROM animal WHERE id = ?", (animal_id,)).fetchone()
    return linha_para_dict(linha)


def criar(tutor_id, dados):
    conexao = obter_conexao()
    cursor = conexao.execute(
        """INSERT INTO animal (tutor_id, nome, especie, raca, idade_anos)
           VALUES (:tutor_id, :nome, :especie, :raca, :idade_anos)""",
        {**dados, "tutor_id": tutor_id},
    )
    conexao.commit()
    return cursor.lastrowid


def atualizar(animal_id, dados):
    conexao = obter_conexao()
    conexao.execute(
        """UPDATE animal
           SET nome = :nome, especie = :especie, raca = :raca, idade_anos = :idade_anos
           WHERE id = :id""",
        {**dados, "id": animal_id},
    )
    conexao.commit()


def excluir(animal_id):
    conexao = obter_conexao()
    conexao.execute("DELETE FROM animal WHERE id = ?", (animal_id,))
    conexao.commit()
