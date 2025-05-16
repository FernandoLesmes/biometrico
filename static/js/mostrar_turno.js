$(document).ready(function () {
    $("#turnosTable").DataTable({
        dom: 'f',
        language: {
            search: "🔍 Buscar:",
            zeroRecords: "No se encontraron registros.",
            infoEmpty: "",
            infoFiltered: "",
            paginate: {
                previous: "",
                next: ""
            }
        }
    });

    $("#abrirModal").click(function () {
        $("#modalTurno").fadeIn();
    });

    $(".close").click(function () {
        $("#modalTurno").fadeOut();
    });
});
