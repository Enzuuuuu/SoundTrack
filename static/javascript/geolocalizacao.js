// Funções de callback para sucesso e erro, como no exemplo anterior.


function sucesso(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // 🚨 PASSO 1: Criar o corpo da requisição no formato de formulário
    const formData = new URLSearchParams();
    formData.append('latitude', latitude);
    formData.append('longitude', longitude);

    fetch("/coordenadas", { 
        method: 'POST',
        headers: {
            // 🚨 PASSO 2: O Content-Type deve ser este para Formulário
            'Content-Type': 'application/x-www-form-urlencoded' 
        },
        // 🚨 PASSO 3: Enviar o corpo como string
        body: formData.toString() 
    })
    .then(response => {
        // Verifica se a resposta HTTP foi OK antes de tentar o JSON
        if (!response.ok) {
            // Se cair aqui, o status é 404, 500, etc.
            throw new Error(`Erro HTTP: Status ${response.status}`);
        }
        return response.json(); 
    })
    .then(data => {
        document.getElementById('resultado').textContent = `Você está em: ${data.address}`;
        document.getElementById('status').textContent = 'Localização obtida com sucesso!';
    })
    .catch(error => {
        // Este é o bloco que captura o SyntaxError/JSON inválido e o Erro HTTP
        document.getElementById('status').textContent = `Erro ao obter endereço: ${error.message}`;
    });
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
