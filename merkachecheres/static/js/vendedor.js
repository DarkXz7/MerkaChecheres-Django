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

    // Formato de precio para pesos colombianos
    const precioInput = document.getElementById('precio');

    precioInput.addEventListener('input', function () {
        let value = this.value.replace(/[^0-9]/g, ''); // Solo números
        if (value) {
            value = new Intl.NumberFormat('es-CO').format(parseInt(value, 10)); // Formato colombiano
        }
        this.value = value;
    });

    precioInput.addEventListener('focus', function () {
        this.setAttribute('data-placeholder', this.placeholder);
        this.placeholder = '';
    });

    precioInput.addEventListener('blur', function () {
        this.placeholder = this.getAttribute('data-placeholder');
    });
});
document.addEventListener('DOMContentLoaded', function () {
    const cancelButton = document.querySelector('.cancel-btn');

    cancelButton.addEventListener('click', function () {
        const redirectUrl = this.getAttribute('data-url'); // Obtener la URL del botón
        window.location.href = redirectUrl; // Redirigir al index
    });
});
