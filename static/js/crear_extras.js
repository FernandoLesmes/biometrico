$(document).ready(function () {
    // 🔹 Abrir modales
    $("#abrirModalCargo").click(function () {
        $("#modalCargo").fadeIn();
        $("#modalCargo h2").text("Agregar Nuevo Cargo");
    });

    $("#abrirModalRol").click(function () {
        $("#modalRol").fadeIn();
        $("#modalRol h2").text("Agregar Nuevo Rol");  // ✅ Corrección aquí
    });

    $("#abrirModalCentroCosto").click(function () {
        $("#modalCentroCosto").fadeIn();
        $("#modalCentroCosto h2").text("Agregar Nuevo Centro de Costo");  // ✅ Corrección aquí
    });

    // 🔹 Cerrar modales
    $(".close-cargo").click(function () {
        $("#modalCargo").fadeOut();
    });

    $(".close-rol").click(function () {
        $("#modalRol").fadeOut();
    });

    $(".close-centro").click(function () {
        $("#modalCentroCosto").fadeOut();
    });
});




// 🔹 Enviar formulario de Cargo
$("#formCrearCargo").submit(function (e) {
    e.preventDefault();
    const nombre = $("#nombreCargo").val();
    const token = $("meta[name='csrf-token']").attr("content");

    $.post("/crear-cargo/", { nombre: nombre, csrfmiddlewaretoken: token }, function (res) {
        if (res.success) {
            alert("✅ Cargo guardado correctamente");
            $("#modalCargo").fadeOut();
            $("#formCrearCargo")[0].reset();
        } else {
            alert("❌ Error al guardar cargo");
        }
    });
});

// 🔹 Enviar formulario de Rol
$("#formCrearRol").submit(function (e) {
    e.preventDefault();
    const nombre = $("#nombreRol").val();
    const token = $("meta[name='csrf-token']").attr("content");

    $.post("/crear-rol/", { nombre: nombre, csrfmiddlewaretoken: token }, function (res) {
        if (res.success) {
            alert("✅ Rol guardado correctamente");
            $("#modalRol").fadeOut();
            $("#formCrearRol")[0].reset();
        } else {
            alert("❌ Error al guardar rol");
        }
    });
});

// 🔹 Enviar formulario de Centro de Costo
$("#formCrearCentro").submit(function (e) {
    e.preventDefault();
    const nombre = $("#nombreCentro").val();
    const token = $("meta[name='csrf-token']").attr("content");

    $.post("/crear-centro-costo/", { nombre: nombre, csrfmiddlewaretoken: token }, function (res) {
        if (res.success) {
            alert("✅ Centro de costo guardado correctamente");
            $("#modalCentroCosto").fadeOut();
            $("#formCrearCentro")[0].reset();
        } else {
            alert("❌ Error al guardar centro de costo");
        }
    });
});
