$(document).ready(function () {
    $("#crearTurnoForm").submit(function (event) {
        event.preventDefault();

        const csrfToken = $("meta[name='csrf-token']").attr("content");

        let data = {
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
            csrfmiddlewaretoken: csrfToken
        };

        $.post("/turnos/crear/", data, function (response) {
            if (response.success) {
                alert("✅ Turno creado con éxito");
                $("#modalTurno").fadeOut();
                $("#crearTurnoForm")[0].reset();

                let tabla = $('#turnosTable').DataTable();
                tabla.row.add([
                    response.id,
                    response.shift_name,
                    response.start_time,
                    response.max_entry_time,
                    response.end_time,
                    response.work_hours,
                    response.break_type,
                    response.break_minutes,
                    response.break_start,
                    response.break_end,
                    `<select class="cambiar-estado ${response.status.toLowerCase()}" data-id="${response.id}">
                        <option value="Activo" ${response.status === 'Activo' ? 'selected' : ''}>Activo</option>
                        <option value="Inactivo" ${response.status === 'Inactivo' ? 'selected' : ''}>Inactivo</option>
                    </select>`,
                    `<button class="editar" data-id="${response.id}">✏️ Editar</button>`
                ]).draw(false);

                // Añadir clase visual
                $(`select[data-id="${response.id}"]`).addClass(response.status.toLowerCase());

            } else {
                alert("❌ Error en la respuesta del servidor");
                console.log("❌ Error:", response.error);
            }
        }).fail(function (error) {
            alert("❌ Error al crear el turno");
            console.log("❌ Error:", error.responseText);
        });
    });
});
