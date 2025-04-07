document.addEventListener("DOMContentLoaded", function () {
    console.log("✅ Script cargado correctamente");

    // ✅ Cargar lista de grupos al inicio
    function cargarGrupos() {
        fetch("/grupos/obtener/")
            .then(response => response.json())
            .then(data => {
                console.log("✅ Datos recibidos:", data);
                let tbody = document.getElementById("gruposBody");
                tbody.innerHTML = ""; // 🔥 Limpiar la tabla antes de actualizar

                if (data.grupos.length > 0) {
                    data.grupos.forEach(grupo => {
                        let fila = `<tr>
                            <td>${grupo.id}</td>
                            <td>${grupo.nombre}</td>
                        </tr>`;
                        tbody.innerHTML += fila;
                    });
                } else {
                    tbody.innerHTML = `<tr><td colspan="2">No hay grupos registrados.</td></tr>`;
                }
            })
            .catch(error => console.error("❌ Error al cargar grupos:", error));
    }

    // ✅ Cargar grupos al inicio
    cargarGrupos();

    // ✅ Abrir y cerrar modal
    let modal = document.getElementById("modalGrupo");
    let btnAbrir = document.getElementById("crearGrupoBtn");
    let btnCerrar = document.querySelector(".close");

    btnAbrir.onclick = function () {
        modal.style.display = "block";
    };

    btnCerrar.onclick = function () {
        modal.style.display = "none";
    };

    window.onclick = function (event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    };

    // ✅ Enviar formulario de creación de grupo
    document.getElementById("formCrearGrupo").addEventListener("submit", function (event) {
        event.preventDefault();

        let formData = new FormData(this);

        fetch("/grupos/crear/", {
            method: "POST",
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            console.log("✅ Grupo creado:", data);

            if (data.success) {
                alert("✅ Grupo creado con éxito");
                modal.style.display = "none";
                document.querySelector("input[name=nombre]").value = ""; // ✅ Limpiar campo
                cargarGrupos();  // 🔥 Recargar los datos después de crear
            } else {
                alert("❌ Error: " + data.error);
            }
        })
        .catch(error => {
            console.error("❌ Error en la petición:", error);
            alert("❌ Error al crear el grupo");
        });
    });
});
