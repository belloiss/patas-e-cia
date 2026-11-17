const corpoTabela = document.getElementById("corpo-tabela");

function descreverQuantidadeDeAnimais(total) {
  if (total === 0) return "Nenhum animal";
  return total === 1 ? "1 animal" : `${total} animais`;
}

function linhaDoTutor(tutor) {
  return `<tr>
    <td>${escaparHtml(tutor.nome)}</td>
    <td>${formatarTelefone(tutor.telefone)}</td>
    <td><a href="animais.html?tutor=${tutor.id}">${descreverQuantidadeDeAnimais(tutor.total_animais)}</a></td>
    <td class="acoes">
      <a class="botao botao--secundario botao--pequeno" href="tutor-form.html?id=${tutor.id}">Editar</a>
      <button class="botao botao--perigo botao--pequeno" data-excluir="${tutor.id}">Excluir</button>
    </td>
  </tr>`;
}

async function carregarTutores() {
  const tutores = await chamarApi("GET", "/api/tutores");
  corpoTabela.innerHTML = tutores.length
    ? tutores.map(linhaDoTutor).join("")
    : `<tr><td colspan="4" class="vazio">Nenhum tutor cadastrado. Cadastre o primeiro para começar.</td></tr>`;
}

corpoTabela.addEventListener("click", async (evento) => {
  const id = evento.target.dataset.excluir;
  if (!id || !confirm("Excluir este tutor?")) return;
  mostrarAviso("");
  try {
    await chamarApi("DELETE", `/api/tutores/${id}`);
    await carregarTutores();
  } catch (erro) {
    mostrarAviso(erro.message);
  }
});

carregarTutores().catch((erro) => mostrarAviso(erro.message));
