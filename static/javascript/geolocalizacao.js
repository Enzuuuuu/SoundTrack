// Funções de callback para sucesso e erro, como no exemplo anterior.


function sucesso(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Seleciona os spans e parágrafos para atualização
    document.getElementById('status').textContent = 'Localização obtida com sucesso!';
}

function erro(err) {
    // Exibe o erro no parágrafo de status
    document.getElementById('status').textContent = `Erro ao obter localização: ${err.message}`;
}


// Função principal chamada pelo botão no HTML (usando onclick="obterLocalizacao()")
function obterLocalizacao() {
    const statusParagrafo = document.getElementById('status');

    statusParagrafo.textContent = 'Buscando localização...';
    
    // Verifica se o navegador suporta a API de Geolocalização
    if (!navigator.geolocation) {
        statusParagrafo.textContent = 'Seu navegador não suporta geolocalização.';
    } else {
        // Solicita a posição: chama 'sucesso' se ok, 'erro' se falhar
        navigator.geolocation.getCurrentPosition(sucesso, erro);
    }
}
window.onload = obterLocalizacao;
