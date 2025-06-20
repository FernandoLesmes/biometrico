document.addEventListener("DOMContentLoaded", function () {
    const filas = document.querySelectorAll("tr[data-id-grupo]");

    filas.forEach(fila => {
        fila.addEventListener("click", function () {
            const grupoId = this.getAttribute("data-id-grupo");

            fetch(`/grupo/${grupoId}/detalle/`)
                .then(response => response.json())
                .then(data => {
                    // Rellenar información del grupo
                    document.getElementById("grupoIdSeleccionado").value = grupoId;
                    document.getElementById("grupoNombre").textContent = data.grupo;
                    document.getElementById("jefePlanta").textContent = data.jefe_planta;
                    document.getElementById("supervisores").innerHTML = data.supervisores.map(s => `<li>${s}</li>`).join('');
                    document.getElementById("empleados").innerHTML = data.empleados.map(e => `<li>${e}</li>`).join('');

                    // Resetear el select de jefe
                    const selectJefe = document.getElementById("selectJefe");
                    if (selectJefe) selectJefe.selectedIndex = 0;

                    // Resetear los seleccionados del select múltiple de supervisores
                    const selectSupervisores = document.getElementById("selectSupervisores");
                    if (selectSupervisores) {
                        [...selectSupervisores.options].forEach(option => {
                            option.selected = false;
                        });
                    }

                    // Mostrar el modal
                    document.getElementById("modalDetalleGrupo").style.display = "block";
                })
                .catch(error => {
                    console.error("❌ Error al cargar detalles del grupo:", error);
                    alert("Error al cargar los datos del grupo.");
                });
        });
    });

    // Cerrar modal de detalle
    const btnCerrar = document.querySelector(".close-detalle");
    if (btnCerrar) {
        btnCerrar.addEventListener("click", () => {
            document.getElementById("modalDetalleGrupo").style.display = "none";
        });
    }
});

document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("formAsignarRoles");

    if (form) {
        form.addEventListener("submit", function (e) {
            const jefeSelect = document.getElementById("selectJefe");
            const supervisoresSelect = document.getElementById("selectSupervisores");

            // ✅ Forzar jefe vacío si no hay valor seleccionado
            if (!jefeSelect.value) {
                const inputJefe = document.createElement("input");
                inputJefe.type = "hidden";
                inputJefe.name = "jefe_planta";
                inputJefe.value = "";
                form.appendChild(inputJefe);
            }

            // ✅ Forzar supervisores vacío si ninguno está seleccionado
            if (supervisoresSelect.selectedOptions.length === 0) {
                const inputSupervisores = document.createElement("input");
                inputSupervisores.type = "hidden";
                inputSupervisores.name = "supervisores";
                inputSupervisores.value = "";
                form.appendChild(inputSupervisores);
            }
        });
    }
});
