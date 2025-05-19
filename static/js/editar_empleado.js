$(document).on("click", ".editar", function () {
    const empleadoId = $(this).data("id");

    $.get(`/empleados/obtener/${empleadoId}/`, function (data) {
        $("input[name=emp_pin]").val(data.emp_pin);
        $("input[name=emp_firstname]").val(data.emp_firstname);
        $("input[name=emp_lastname]").val(data.emp_lastname);
        $("select[name=emp_job]").val(data.emp_job);
        $("select[name=emp_group]").val(data.emp_group);
        $("select[name=emp_role]").val(data.emp_role);
        $("select[name=emp_cost_center]").val(data.emp_cost_center);
        $("input[name=emp_email]").val(data.emp_email);
        $("input[name=emp_active]").prop("checked", data.emp_active);

        // Mostrar modal y cambiar título
        $("#modalEmpleado").fadeIn();
        $(".modal-content h2").text("Editar Empleado");

        // Cambiar submit
        $("form").off("submit").on("submit", function (e) {
            e.preventDefault();

            const datos = {
                emp_pin: $("input[name=emp_pin]").val(),
                emp_firstname: $("input[name=emp_firstname]").val(),
                emp_lastname: $("input[name=emp_lastname]").val(),
                emp_job: $("select[name=emp_job]").val(),
                emp_group: $("select[name=emp_group]").val(),
                emp_role: $("select[name=emp_role]").val(),
                emp_cost_center: $("select[name=emp_cost_center]").val(),
                emp_email: $("input[name=emp_email]").val(),
                emp_active: $("input[name=emp_active]").is(":checked"),
                csrfmiddlewaretoken: $("meta[name='csrf-token']").attr("content")
            };

            $.post(`/empleados/editar/${empleadoId}/`, datos, function (response) {
                if (response.success) {
                    alert("✅ Empleado actualizado correctamente");
                    location.reload();
                } else {
                    alert("❌ Error al actualizar");
                }
            }).fail(function () {
                alert("❌ Error de conexión al servidor");
            });
        });
    });
});
