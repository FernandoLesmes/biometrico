$(document).on("click", ".editar", function () {
    const turnoId = $(this).data("id");

    $.get(`/turnos/editar/${turnoId}/`, function (data) {
        // Llena los campos del formulario con los datos del turno
        $("#nombre").val(data.shift_name);
        $("#entrada").val(data.start_time);
        $("#max_entrada").val(data.max_entry_time);
        $("#salida").val(data.end_time);
        $("#horas").val(data.work_hours);
        $("#descanso").val(data.break_type);
        $("#minutos_descanso").val(data.break_minutes);
        $("#inicio_descanso").val(data.break_start || "00:00");
        $("#fin_descanso").val(data.break_end || "00:00");
        $("#estado").val(data.status);

        // Muestra el modal
        $("#modalTurno").fadeIn();
        $(".modal-content h2").text("Editar Turno");


        // Cambia el comportamiento del botón para guardar edición
        $("#crearTurnoForm").off("submit").on("submit", function (e) {
            e.preventDefault();

            const updatedData = {
                shift_name: $("#nombre").val(),
                start_time: $("#entrada").val(),
                max_entry_time: $("#max_entrada").val(),
                end_time: $("#salida").val(),
                work_hours: $("#horas").val(),
                break_type: $("#descanso").val(),
                break_minutes: $("#minutos_descanso").val(),
                break_start: $("#inicio_descanso").val() || "00:00",
                break_end: $("#fin_descanso").val() || "00:00",
                status: $("#estado").val(),
                csrfmiddlewaretoken: $("meta[name='csrf-token']").attr("content")
            };

            $.post(`/turnos/editar/${turnoId}/`, updatedData, function (response) {
                if (response.success) {
                    alert("✅ Turno actualizado correctamente");
                    location.reload();
                } else {
                    alert("❌ Error al actualizar turno");
                }
            }).fail(function (error) {
                alert("❌ Error técnico");
                console.log("Error:", error.responseText);
            });
        });
    });
});
