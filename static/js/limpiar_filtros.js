document.addEventListener("DOMContentLoaded", function () {
  const form = document.querySelector("form.formulario-filtros");

  if (form) {
    window.addEventListener("pageshow", function () {
      // 🔹 Limpiar inputs de texto y fecha
      const inputs = form.querySelectorAll("input[type='text'], input[type='date']");
      inputs.forEach(input => {
        input.value = "";
      });

      // 🔹 Limpiar selects (como tipo de reporte)
      const selects = form.querySelectorAll("select");
      selects.forEach(select => {
        select.selectedIndex = 0; // Primer valor del select
      });
    });
  }
});

