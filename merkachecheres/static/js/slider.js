let currentIndex = 0;

function moveSlide(direction) {
    const carousel = document.querySelector('.carousel');
    const totalSlides = document.querySelectorAll('.seller_card').length;
    const slideWidth = document.querySelector('.seller_card').offsetWidth + 20; // Ajusta el tamaño según tu margen

    // Actualizar el índice
    currentIndex += direction;

    // Evitar que se salga del rango
    if (currentIndex < 0) {
        currentIndex = totalSlides - 1; // Volver al final
    } else if (currentIndex >= totalSlides) {
        currentIndex = 0; // Volver al inicio
    }

    // Aplicar el desplazamiento
    carousel.style.transform = `translateX(-${currentIndex * slideWidth}px)`;
}

