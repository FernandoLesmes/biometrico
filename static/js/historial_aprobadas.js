// ✅ Esta función va al principio
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("modal-historial");
    const btn = document.getElementById("btn-ver-historial");
    const span = document.getElementById("cerrar-modal");
    const tbody = document.querySelector("#tabla-historial tbody");

    if (btn && modal && span && tbody) {
        btn.onclick = function () {
            console.log("🟢 Click en botón historial");

            fetch("/historial-horas-extras/ajax/")
                .then(response => response.json())
                .then(data => {
                    console.log("📦 Datos:", data);
                    tbody.innerHTML = "";
                    data.forEach(r => {
                        const fila = `
                            <tr>
                                <td>${r.cedula}</td>
                                <td>${r.apellidos}</td>
                                <td>${r.nombre}</td>
                                <td>${r.grupo}</td>
                                <td>${r.fecha}</td>
                                <td>${r.turno}</td>
                                <td>${r.entrada}</td>
                                <td>${r.salida}</td>
                                <td>${r.horas_extras_diurnas}</td>
                                <td>${r.horas_extras_nocturnas}</td>
                                <td>${r.horas_extras_festivas_diurnas}</td>
                                <td>${r.horas_extras_festivas_nocturnas}</td>
                                <td>${r.recargo_nocturno}</td>
                                <td>${r.recargo_nocturno_festivo}</td>
                                <td>${r.supervisor}</td>
                                <td>${r.jefe}</td>
                                <td>
                                    <input type="checkbox" class="bloqueado-checkbox" data-id="${r.id_turno}" ${r.bloqueado === 1 ? "checked" : ""}>
                                </td>
                            </tr>
                        `;
                        tbody.innerHTML += fila;
                    });

                    modal.style.display = "block";
                });
        };

        span.onclick = function () {
            modal.style.display = "none";
        };

        window.onclick = function (event) {
            if (event.target === modal) {
                modal.style.display = "none";
            }
        };
    }
});

document.addEventListener("change", function (e) {
    if (e.target.classList.contains("bloqueado-checkbox")) {
        const turnoId = e.target.getAttribute("data-id");
        const value = e.target.checked;

        fetch("/reportes/aprobar/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({
                id: turnoId,
                field: "bloqueado_para_pago",
                value: value,
            }),
        })
        .then(r => r.json())
        .then(data => {
            if (!data.success) {
                alert("❌ " + data.error);
                e.target.checked = !value;
            }
        })
        .catch(error => {
            console.error("Error al enviar datos:", error);
            alert("❌ Error inesperado al guardar cambios.");
        });
    }
});
