const abrir = document.querySelectorAll(".perguntas dt");
const resposta = document.querySelectorAll(".perguntas dd");
abrir.forEach(eventoPerguntas);
function eventoPerguntas(pergunta) {
  pergunta.addEventListener("click", mostrarResposta);
}
function mostrarResposta(event) {
  const pergunta = event.currentTarget;
  pergunta.classList.toggle("abrir");
}




