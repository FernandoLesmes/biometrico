document.addEventListener("DOMContentLoaded", function () {
    document.querySelectorAll("input[type='checkbox'][data-id]").forEach(function (checkbox) {
        checkbox.addEventListener("change", function () {
            const id = this.getAttribute("data-id");
            const field = this.getAttribute("data-field");
            const value = this.checked;

            fetch("/reportes/aprobar/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({ id: id, field: field, value: value })
            })
            .then(response => response.json())
            .then(data => {
                if (!data.success) {
                    alert("❌ Error: " + data.error);
                    this.checked = !value;  // Revertir cambio si hubo error
                }
            });
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== "") {
            const cookies = document.cookie.split(";");
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + "=")) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});
