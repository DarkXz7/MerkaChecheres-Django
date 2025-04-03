// Función para abrir la sidebar
function openNav() {
    document.getElementById("mySidebar").style.width = "250px"; // Ajusta el ancho de la sidebar
    document.getElementById("main-content").style.marginLeft = "250px"; // Mueve el contenido principal
}

// Función para cerrar la sidebar
function closeNav() {
    document.getElementById("mySidebar").style.width = "0"; // Cierra la sidebar
    document.getElementById("main-content").style.marginLeft = "0"; // Restablece el contenido principal
}
