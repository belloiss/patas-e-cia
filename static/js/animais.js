const tutorId = lerParametro("tutor");
const corpoTabela = document.getElementById("corpo-tabela");

document.getElementById("novo-animal").href = `animal-form.html?tutor=${tutorId}`;

function linhaDoAnimal(animal) {
  const idade = animal.idade_anos === null ? "—" : `${animal.idade_anos} ano(s)`;
  return `<tr>
    <td>${escaparHtml(animal.nome)}</td>
    <td>${escaparHtml(animal.especie)}</td>
    <td>${escaparHtml(animal.raca) || "—"}</td>
    <td>${idade}</td>
    <td class="acoes">
      <a class="botao botao--secundario botao--pequeno" href="animal-form.html?tutor=${tutorId}&id=${animal.id}">Editar</a>
      <button class="botao botao--perigo botao--pequeno" data-excluir="${animal.id}">Excluir</button>
    </td>
  </tr>`;
}

async function carregarAnimais() {
  const animais = await chamarApi("GET", `/api/tutores/${tutorId}/animais`);
  corpoTabela.innerHTML = animais.length
    ? animais.map(linhaDoAnimal).join("")
    : `<tr><td colspan="5" class="vazio">Este tutor ainda não tem animais. Use "Novo animal" para cadastrar.</td></tr>`;
}

async function carregarTutor() {
  const tutor = await chamarApi("GET", `/api/tutores/${tutorId}`);
  document.getElementById("titulo").textContent = `Animais de ${tutor.nome}`;
  document.getElementById("contato").textContent = formatarTelefone(tutor.telefone);
}

corpoTabela.addEventListener("click", async (evento) => {
  const id = evento.target.dataset.excluir;
  if (!id || !confirm("Excluir este animal?")) return;
  try {
    await chamarApi("DELETE", `/api/animais/${id}`);
    await carregarAnimais();
  } catch (erro) {
    mostrarAviso(erro.message);
  }
});

Promise.all([carregarTutor(), carregarAnimais()]).catch((erro) => mostrarAviso(erro.message));
