async function chamarApi(metodo, url, corpo) {
  const resposta = await fetch(url, {
    method: metodo,
    headers: { "Content-Type": "application/json" },
    body: corpo ? JSON.stringify(corpo) : undefined,
  });
  if (resposta.status === 204) return null;

  const dados = await resposta.json().catch(() => ({}));
  if (!resposta.ok) {
    const erro = new Error(dados.erro || "Não foi possível concluir a operação.");
    erro.campos = dados.campos || {};
    throw erro;
  }
  return dados;
}

function lerParametro(nome) {
  return new URLSearchParams(location.search).get(nome);
}

function escaparHtml(texto) {
  const elemento = document.createElement("div");
  elemento.textContent = texto ?? "";
  return elemento.innerHTML;
}

function formatarTelefone(digitos) {
  if (digitos.length === 11) return `(${digitos.slice(0, 2)}) ${digitos.slice(2, 7)}-${digitos.slice(7)}`;
  if (digitos.length === 10) return `(${digitos.slice(0, 2)}) ${digitos.slice(2, 6)}-${digitos.slice(6)}`;
  return digitos;
}

function mostrarAviso(mensagem) {
  const aviso = document.getElementById("aviso");
  aviso.textContent = mensagem || "";
  aviso.hidden = !mensagem;
}

function limparErrosDosCampos() {
  document.querySelectorAll("[data-erro]").forEach((el) => (el.textContent = ""));
  document.querySelectorAll("[aria-invalid]").forEach((el) => el.removeAttribute("aria-invalid"));
}

function mostrarErrosDosCampos(campos) {
  Object.entries(campos).forEach(([nome, mensagem]) => {
    const destino = document.querySelector(`[data-erro="${nome}"]`);
    const entrada = document.querySelector(`[name="${nome}"]`);
    if (destino) destino.textContent = mensagem;
    if (entrada) entrada.setAttribute("aria-invalid", "true");
  });
}

function ligarFormulario(formulario, salvar, destinoAposSalvar) {
  formulario.addEventListener("submit", async (evento) => {
    evento.preventDefault();
    mostrarAviso("");
    limparErrosDosCampos();
    try {
      await salvar(Object.fromEntries(new FormData(formulario)));
      location.href = destinoAposSalvar();
    } catch (erro) {
      mostrarAviso(erro.message);
      mostrarErrosDosCampos(erro.campos || {});
    }
  });
}

function preencherFormulario(formulario, dados) {
  Object.entries(dados).forEach(([nome, valor]) => {
    const campo = formulario.elements[nome];
    if (campo) campo.value = valor ?? "";
  });
}
