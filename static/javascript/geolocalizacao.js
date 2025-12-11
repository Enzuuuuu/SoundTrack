// Funções de callback para sucesso e erro, como no exemplo anterior.
console.log("Arquivo JS carregado!");

function sucesso(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // Seleciona os spans e parágrafos para atualização
    document.getElementById('status').textContent = 'Localização obtida com sucesso!';
    document.getElementById('latitude').textContent = latitude.toFixed(6);
    document.getElementById('longitude').textContent = longitude.toFixed(6);

    // Cria e exibe o link para o mapa
    const mapLink = document.getElementById('map-link');
    mapLink.href = `https://www.openstreetmap.org/#map=16/${latitude}/${longitude}`;
    mapLink.textContent = `Ver no OpenStreetMap`;
    mapLink.style.display = 'inline'; // Torna o link visível
}

function erro(err) {
    // Exibe o erro no parágrafo de status
    document.getElementById('status').textContent = `Erro ao obter localização: ${err.message}`;
    document.getElementById('map-link').style.display = 'none'; // Esconde o link se der erro
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
