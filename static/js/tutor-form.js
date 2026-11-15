const formulario = document.getElementById("formulario");
const tutorId = lerParametro("id");

if (tutorId) {
  document.getElementById("titulo").textContent = "Editar tutor";
  chamarApi("GET", `/api/tutores/${tutorId}`)
    .then((tutor) => preencherFormulario(formulario, { ...tutor, telefone: formatarTelefone(tutor.telefone) }))
    .catch((erro) => mostrarAviso(erro.message));
}

ligarFormulario(
  formulario,
  (dados) => (tutorId ? chamarApi("PUT", `/api/tutores/${tutorId}`, dados) : chamarApi("POST", "/api/tutores", dados)),
  () => "index.html"
);
