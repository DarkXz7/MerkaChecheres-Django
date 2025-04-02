document.addEventListener('DOMContentLoaded', function () {
    const fileInput = document.getElementById('imagen');
    const previewContainer = document.getElementById('preview-container');

    // Inicializar 12 espacios con el signo "+"
    previewContainer.innerHTML = '';
    for (let i = 0; i < 12; i++) {
        const placeholder = document.createElement('div');
        placeholder.textContent = '+';
        placeholder.classList.add('placeholder');
        placeholder.onclick = function () {
            fileInput.click();
        };
        previewContainer.appendChild(placeholder);
    }

    fileInput.addEventListener('change', function (event) {
        const files = event.target.files;
        const placeholders = document.querySelectorAll('.placeholder');

        Array.from(files).forEach((file, index) => {
            if (index >= placeholders.length) return; // No exceder el límite de 12 imágenes
            const reader = new FileReader();
            reader.onload = function (e) {
                const imgContainer = placeholders[index];
                imgContainer.innerHTML = '';
                imgContainer.classList.remove('placeholder');
                imgContainer.classList.add('image-container');
                
                const img = document.createElement('img');
                img.src = e.target.result;
                img.style.width = '100%';
                img.style.height = '100%';
                img.style.objectFit = 'cover';

                const removeBtn = document.createElement('button');
                removeBtn.textContent = 'X';
                removeBtn.classList.add('remove-btn');
                removeBtn.onclick = function (event) {
                    event.stopPropagation();
                    imgContainer.innerHTML = '+';
                    imgContainer.classList.remove('image-container');
                    imgContainer.classList.add('placeholder');
                };

                imgContainer.appendChild(img);
                imgContainer.appendChild(removeBtn);
            };
            reader.readAsDataURL(file);
        });
    });

    const precioInput = document.getElementById('precio');
precioInput.type = "text"; 

precioInput.addEventListener('input', function () {
    let value = this.value.replace(/[^0-9]/g, ''); // Solo números
    if (value.length > 10) {
        value = value.slice(0, 10); // Evita que se excedan los 10 dígitos
    }
    this.value = value;
});

// Convertir el precio antes de enviar el formulario
document.querySelector('form').addEventListener('submit', function (event) {
    let rawValue = precioInput.value.replace(/\./g, ''); // Eliminar puntos
    if (!rawValue.match(/^\d+$/)) { // Validar que solo haya números
        event.preventDefault();
        alert('Ingrese un precio válido.');
        return;
    }
    if (rawValue.length > 10) { // Máximo permitido
        event.preventDefault();
        alert('El precio no puede superar 99999999.99.');
        return;
    }
    precioInput.value = (parseInt(rawValue) / 100).toFixed(2); // Formato decimal
});


    // Evitar que el usuario ingrese letras o caracteres inválidos
    precioInput.addEventListener('keydown', function (event) {
        if (!/^[0-9]$/.test(event.key) && event.key !== 'Backspace' && event.key !== 'Delete' && event.key !== 'ArrowLeft' && event.key !== 'ArrowRight' && event.key !== 'Tab') {
            event.preventDefault();
        }
    });

    // Funcionalidad del botón cancelar
    const cancelButton = document.querySelector('.cancel-btn');
    if (cancelButton) {
        cancelButton.addEventListener('click', function () {
            const redirectUrl = this.getAttribute('data-url') || '/'; // Redirigir al index
            window.location.href = redirectUrl;
        });
    }
});