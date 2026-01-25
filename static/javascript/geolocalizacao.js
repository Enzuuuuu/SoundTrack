
function erro(err) {
    document.getElementById("status").classList.add("erro");
    document.getElementById("status").textContent =
        `Erro ao obter localização: ${err.message}`;
}

//se conseguir a geolocalização
function sucesso(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    const mapaLink = document.getElementById("map-link");
    //gera um link para o streetview com a localização de quem está usando o site
    mapaLink.href = `https://www.google.com/maps?q=${latitude},${longitude}`;
    
    const formData = new URLSearchParams();
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);
     

    //chama a função distancia de funcoes.py com o método post ( ATRAVÉS DE UM JSON )
    fetch("/distancia", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            latitude: latitude,
            longitude: longitude
        })
    })
    .then(r => r.json())
    .then(data => {
        document.querySelectorAll(".distancia").forEach(td => {
            const titulo = td.dataset.titulo;
            const show = data.find(s => s.titulo === titulo);
            //devolve mensagens de sucesso
            document.getElementById("status").textContent =
                "Localização obtida com sucesso.";
            document.getElementById("status").classList.add("sucesso");
            if (show) {
                td.textContent = show.distancia_km + " km";
            }
        });
    })
    .catch(err => {
        //devolve mensagem de erro
        document.getElementById("status").textContent =
            `Erro ao obter endereço: ${err.message}`;
        document.getElementById("status").classList.add("erro");
    });
}


// Assim que a pagina carrega ela chama essa função
window.addEventListener("load", () => {
    const statusParagrafo = document.getElementById("status");
    statusParagrafo.textContent = "Buscando localização...";
    //confere se há suporte para geolocalização
    if (!navigator.geolocation) {
        statusParagrafo.textContent =
            "Seu navegador não suporta geolocalização.";
        return;
    }
    //chama a função de geolocalização
    navigator.geolocation.getCurrentPosition(sucesso, erro);
});

