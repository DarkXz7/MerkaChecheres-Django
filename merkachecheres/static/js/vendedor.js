document.addEventListener('DOMContentLoaded', function() {
    const fileInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('preview-container');

    fileInput.addEventListener('change', function(event) {
        const files = event.target.files; // Capturar todas las imágenes seleccionadas
        previewContainer.innerHTML = ''; // Limpiar cualquier previsualización anterior

        Array.from(files).forEach(file => {
            const reader = new FileReader();
            reader.onload = function(e) {
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
});

