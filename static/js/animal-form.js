const formulario = document.getElementById("formulario");
const tutorId = lerParametro("tutor");
const animalId = lerParametro("id");

document.getElementById("voltar").href = `animais.html?tutor=${tutorId}`;
document.getElementById("cancelar").href = `animais.html?tutor=${tutorId}`;

if (animalId) {
  document.getElementById("titulo").textContent = "Editar animal";
  chamarApi("GET", `/api/animais/${animalId}`)
    .then((animal) => preencherFormulario(formulario, animal))
    .catch((erro) => mostrarAviso(erro.message));
}

ligarFormulario(
  formulario,
  (dados) =>
    animalId
      ? chamarApi("PUT", `/api/animais/${animalId}`, dados)
      : chamarApi("POST", `/api/tutores/${tutorId}/animais`, dados),
  () => `animais.html?tutor=${tutorId}`
);
