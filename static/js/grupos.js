document.addEventListener("DOMContentLoaded", function () {
    const filas = document.querySelectorAll("tr[data-id-grupo]");

    filas.forEach(fila => {
        fila.addEventListener("click", function () {
            const grupoId = this.getAttribute("data-id-grupo");

            fetch(`/grupo/${grupoId}/detalle/`)
                .then(response => response.json())
                .then(data => {
                    document.getElementById("grupoNombre").textContent = data.grupo;
                    document.getElementById("jefePlanta").textContent = data.jefe_planta;
                    document.getElementById("supervisores").innerHTML = data.supervisores.map(s => `<li>${s}</li>`).join('');
                    document.getElementById("empleados").innerHTML = data.empleados.map(e => `<li>${e}</li>`).join('');
                    document.getElementById("modalDetalleGrupo").style.display = "block";
                    

                });
        });
    });

    document.getElementById("cerrarModal").addEventListener("click", () => {
        document.getElementById("modalGrupo").style.display = "none";
    });
});
