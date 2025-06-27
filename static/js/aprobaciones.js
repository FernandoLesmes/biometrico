document.addEventListener("DOMContentLoaded", function () {
    const cambiosPendientes = [];

    document.querySelectorAll("input[type='checkbox'][data-id]").forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const id = this.getAttribute("data-id");
            const field = this.getAttribute("data-field");
            const value = this.checked;

            // Guarda cambio en lista temporal
            const index = cambiosPendientes.findIndex(c => c.id === id && c.field === field);
            if (index >= 0) {
                cambiosPendientes[index].value = value;
            } else {
                cambiosPendientes.push({ id, field, value });
            }
        });
    });

    document.getElementById("btn-guardar-cambios").addEventListener("click", function () {
        if (cambiosPendientes.length === 0) {
            alert("⚠️ No hay cambios para guardar.");
            return;
        }

        // Enviar cambios uno por uno
        cambiosPendientes.forEach(cambio => {
            fetch("/reportes/aprobar/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify(cambio)
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("❌ Error: " + data.error);
                }
            });
        });

        alert("✅ Cambios guardados correctamente");
        cambiosPendientes.length = 0; // Limpia lista
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
