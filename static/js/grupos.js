document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ JS cargado correctamente");

    /** ===========================================================
     * 1. Cargar detalles de grupo al hacer clic en fila
     * =========================================================== */
    document.querySelectorAll("tr[data-id-grupo]").forEach(fila => {
        fila.addEventListener("click", () => {
            const grupoId = fila.getAttribute("data-id-grupo");

            fetch(`/grupo/${grupoId}/detalle/`)
                .then(res => res.json())
                .then(data => {
                    // Mostrar datos del grupo
                    document.getElementById("grupoIdSeleccionado").value = grupoId;
                    document.getElementById("grupoNombre").textContent = data.grupo;

                    // Mostrar jefes de planta
                    document.getElementById("jefePlanta").innerHTML = data.jefes_planta
                        .map(j => `<li>${j.nombre}</li>`)
                        .join('') || "<li>-- Ninguno --</li>";

                    // Mostrar supervisores
                    document.getElementById("supervisores").innerHTML = data.supervisores
                        .map(s => `<li>${s.nombre}</li>`)
                        .join('') || "<li>-- Ninguno --</li>";

                    // Mostrar empleados
                    document.getElementById("empleados").innerHTML = data.empleados
                        .map(e => `<li>${e}</li>`)
                        .join('') || "<li>-- Ninguno --</li>";

                    // ================================
                    // SELECCIONAR EN LOS SELECTS
                    // ================================
                    const selectJefe = document.getElementById("selectJefe");
                    if (selectJefe) {
                        // Solo uno permitido
                        if (data.jefes_planta.length > 0) {
                            selectJefe.value = data.jefes_planta[0].id;
                        } else {
                            selectJefe.value = "";
                        }
                    }

                    const selectSupervisores = document.getElementById("selectSupervisores");
                    if (selectSupervisores) {
                        // Desmarcar todo
                        Array.from(selectSupervisores.options).forEach(opt => opt.selected = false);

                        // Marcar supervisores existentes
                        data.supervisores.forEach(s => {
                            const match = Array.from(selectSupervisores.options).find(opt => opt.value == s.id);
                            if (match) match.selected = true;
                        });
                    }

                    // Abrir el modal
                    document.getElementById("modalDetalleGrupo").style.display = "block";
                })
                .catch(error => {
                    console.error("❌ Error al cargar detalles:", error);
                    alert("❌ Error al cargar los datos del grupo.");
                });
        });
    });

    /** ===========================================================
     * 2. Cerrar modal de detalle
     * =========================================================== */
    const btnCerrar = document.querySelector(".close-detalle");
    if (btnCerrar) {
        btnCerrar.addEventListener("click", () => {
            document.getElementById("modalDetalleGrupo").style.display = "none";
        });
    }

    /** ===========================================================
     * 3. Enviar formulario de ASIGNAR ROLES (jefe y supervisores)
     * =========================================================== */
    const formAsignar = document.getElementById("formAsignarRoles");
    if (formAsignar) {
        formAsignar.addEventListener("submit", e => {
            e.preventDefault();

            const grupoId = document.getElementById("grupoIdSeleccionado").value;
            if (!grupoId) {
                alert("❌ No se ha seleccionado ningún grupo.");
                return;
            }

            // ✅ Prepara datos
            const formData = new FormData();

            const jefeId = document.getElementById("selectJefe").value;
            if (jefeId) {
                formData.append("jefe_planta", jefeId);
            }

            const supervisoresSelect = document.getElementById("selectSupervisores");
            Array.from(supervisoresSelect.selectedOptions).forEach(opt => {
                formData.append("supervisores", opt.value);
            });

            // ✅ CSRF token
            const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;
            formData.append("csrfmiddlewaretoken", csrfToken);

            // ✅ Enviar
            fetch(`/grupo/${grupoId}/asignar_roles/`, {
                method: "POST",
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert("✅ Roles asignados correctamente");
                        document.getElementById("modalDetalleGrupo").style.display = "none";
                        location.reload();  // Opcional si quieres recargar la tabla
                    } else {
                        alert("❌ Error: " + (data.error || "No se pudo guardar."));
                    }
                })
                .catch(() => {
                    alert("❌ Error en la solicitud. Verifica tu conexión o el servidor.");
                });
        });
    }

    /** ===========================================================
     * 4. Crear grupo nuevo (modal de crear)
     * =========================================================== */
    const btnAbrir = document.getElementById("crearGrupoBtn");
    const modalCrear = document.getElementById("modalGrupo");
    const btnCerrarCrear = document.querySelector(".close");

    if (btnAbrir && modalCrear && btnCerrarCrear) {
        btnAbrir.onclick = () => modalCrear.style.display = "block";
        btnCerrarCrear.onclick = () => modalCrear.style.display = "none";
        window.onclick = e => {
            if (e.target == modalCrear) modalCrear.style.display = "none";
        };
    }

    const formCrear = document.getElementById("formCrearGrupo");
    if (formCrear) {
        formCrear.addEventListener("submit", e => {
            e.preventDefault();

            const formData = new FormData(formCrear);
            fetch("/grupos/crear/", {
                method: "POST",
                body: formData
            })
                .then(res => res.json())
                .then(data => {
                    if (data.success) {
                        alert("✅ Grupo creado con éxito");
                        modalCrear.style.display = "none";
                        location.reload();
                    } else {
                        alert("❌ Error: " + (data.error || "No se pudo crear."));
                    }
                })
                .catch(() => {
                    alert("❌ Error al crear el grupo.");
                });
        });
    }
});
