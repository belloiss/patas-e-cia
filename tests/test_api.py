import os
import tempfile
import unittest

from app import create_app, database

TUTOR_VALIDO = {"nome": "Maria Souza", "telefone": "(85) 98888-7777", "email": "maria@exemplo.com"}
ANIMAL_VALIDO = {"nome": "Thor", "especie": "Cão", "raca": "Vira-lata", "idade_anos": 3}


class ApiTestCase(unittest.TestCase):
    def setUp(self):
        self.arquivo = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
        self.arquivo.close()
        self.app = create_app({"DATABASE_URL": f"sqlite:///{self.arquivo.name}", "TESTING": True})
        self.client = self.app.test_client()

    def tearDown(self):
        database.encerrar_banco(self.app)
        os.unlink(self.arquivo.name)

    def criar_tutor(self, dados=None):
        resposta = self.client.post("/api/tutores", json=dados or TUTOR_VALIDO)
        self.assertEqual(resposta.status_code, 201)
        return resposta.get_json()

    def criar_animal(self, tutor_id, dados=None):
        resposta = self.client.post(f"/api/tutores/{tutor_id}/animais", json=dados or ANIMAL_VALIDO)
        self.assertEqual(resposta.status_code, 201)
        return resposta.get_json()


class TutorTests(ApiTestCase):
    def test_crud_completo_de_tutor(self):
        tutor = self.criar_tutor()
        self.assertEqual(tutor["telefone"], "85988887777")

        self.assertEqual(len(self.client.get("/api/tutores").get_json()), 1)

        resposta = self.client.put(f"/api/tutores/{tutor['id']}", json={**TUTOR_VALIDO, "nome": "Maria Lima"})
        self.assertEqual(resposta.get_json()["nome"], "Maria Lima")

        self.assertEqual(self.client.delete(f"/api/tutores/{tutor['id']}").status_code, 204)
        self.assertEqual(self.client.get(f"/api/tutores/{tutor['id']}").status_code, 404)

    def test_campos_obrigatorios(self):
        resposta = self.client.post("/api/tutores", json={})
        self.assertEqual(resposta.status_code, 400)
        campos = resposta.get_json()["campos"]
        self.assertIn("nome", campos)
        self.assertIn("telefone", campos)

    def test_telefone_invalido(self):
        for telefone in ("12345", "(85) 3333-444", "(85) 88888-7777", "(05) 98888-7777"):
            resposta = self.client.post("/api/tutores", json={**TUTOR_VALIDO, "telefone": telefone})
            self.assertEqual(resposta.status_code, 400, telefone)
            self.assertIn("telefone", resposta.get_json()["campos"])

    def test_telefone_fixo_valido(self):
        resposta = self.client.post("/api/tutores", json={**TUTOR_VALIDO, "telefone": "(85) 3333-4444"})
        self.assertEqual(resposta.status_code, 201)

    def test_email_invalido(self):
        resposta = self.client.post("/api/tutores", json={**TUTOR_VALIDO, "email": "sem-arroba"})
        self.assertIn("email", resposta.get_json()["campos"])

    def test_nao_exclui_tutor_com_animais(self):
        tutor = self.criar_tutor()
        animal = self.criar_animal(tutor["id"])

        resposta = self.client.delete(f"/api/tutores/{tutor['id']}")
        self.assertEqual(resposta.status_code, 409)
        self.assertIn("animal", resposta.get_json()["erro"])

        self.client.delete(f"/api/animais/{animal['id']}")
        self.assertEqual(self.client.delete(f"/api/tutores/{tutor['id']}").status_code, 204)


class AnimalTests(ApiTestCase):
    def test_crud_completo_de_animal(self):
        tutor = self.criar_tutor()
        animal = self.criar_animal(tutor["id"])
        self.assertEqual(animal["tutor_id"], tutor["id"])

        lista = self.client.get(f"/api/tutores/{tutor['id']}/animais").get_json()
        self.assertEqual([a["nome"] for a in lista], ["Thor"])

        resposta = self.client.put(f"/api/animais/{animal['id']}", json={**ANIMAL_VALIDO, "nome": "Rex"})
        self.assertEqual(resposta.get_json()["nome"], "Rex")

        self.assertEqual(self.client.delete(f"/api/animais/{animal['id']}").status_code, 204)
        self.assertEqual(self.client.get(f"/api/animais/{animal['id']}").status_code, 404)

    def test_validacao_de_animal(self):
        tutor = self.criar_tutor()
        resposta = self.client.post(
            f"/api/tutores/{tutor['id']}/animais", json={"nome": "", "especie": "Dragão", "idade_anos": 99}
        )
        self.assertEqual(resposta.status_code, 400)
        campos = resposta.get_json()["campos"]
        self.assertEqual(set(campos), {"nome", "especie", "idade_anos"})

    def test_animal_de_tutor_inexistente(self):
        resposta = self.client.post("/api/tutores/999/animais", json=ANIMAL_VALIDO)
        self.assertEqual(resposta.status_code, 404)

    def test_rota_inexistente_retorna_json(self):
        resposta = self.client.get("/api/nada")
        self.assertEqual(resposta.status_code, 404)
        self.assertIn("erro", resposta.get_json())


if __name__ == "__main__":
    unittest.main()
