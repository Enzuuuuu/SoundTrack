// ======================
// Callback de erro
// ======================
function erro(err) {
    document.getElementById("status").textContent =
        `Erro ao obter localização: ${err.message}`;
}

// ======================
// Callback de sucesso
// ======================
function sucesso(position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;

    // ---------- FETCH 1: endereço ----------
    const formData = new URLSearchParams();
    formData.append("latitude", latitude);
    formData.append("longitude", longitude);

    fetch("/coordenadas", {
        method: "POST",
        headers: {
            "Content-Type": "application/x-www-form-urlencoded"
        },
        body: formData.toString()
    })
    .then(r => r.json())
    .then(data => {
        document.getElementById("resultado").textContent =
            `Você está em: ${data.address}`;
        document.getElementById("status").textContent =
            "Localização obtida com sucesso!";
    })
    .catch(err => {
        document.getElementById("status").textContent =
            `Erro ao obter endereço: ${err.message}`;
    });

    // ---------- FETCH 2: distâncias ----------
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

            if (show) {
                td.textContent = show.distancia_km + " km";
            }
        });
    })
    .catch(err => console.error("Erro:", err));
}

window.addEventListener("load", () => {
    const statusParagrafo = document.getElementById("status");
    statusParagrafo.textContent = "Buscando localização...";

    if (!navigator.geolocation) {
        statusParagrafo.textContent =
            "Seu navegador não suporta geolocalização.";
        return;
    }

    navigator.geolocation.getCurrentPosition(sucesso, erro);
});