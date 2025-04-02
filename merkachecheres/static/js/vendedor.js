document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('preview-container');

    fileInput.addEventListener('change', function (event) {
        const files = event.target.files; // Capturar todas las imágenes seleccionadas
        previewContainer.innerHTML = ''; // Limpiar cualquier previsualización anterior

        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function (e) {
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100px';
                img.style.height = '100px';
                img.style.margin = '5px';
                previewContainer.appendChild(img);
            };
            reader.readAsDataURL(file);
        });
    });

    // Formato de precio para añadir decimales y permitir cifras grandes
    const precioInput = document.getElementById('precio');

    precioInput.addEventListener('input', function () {
        let value = this.value.replace(/[^0-9]/g, ''); // Eliminar caracteres no numéricos
        if (value) {
            // Dividir por 100 para agregar decimales
            value = (parseFloat(value) / 100).toFixed(2);
            // Formatear con separadores de miles
            this.value = value.replace(/\B(?=(\d{3})+(?!\d))/g, ',');
        }
    });

    precioInput.addEventListener('blur', function () {
        if (!this.value) {
            this.value = '0.00'; // Si el campo está vacío, establecer un valor predeterminado
        }
    });

    precioInput.addEventListener('focus', function () {
        this.value = this.value.replace(/,/g, ''); // Eliminar comas al enfocar
    });
});