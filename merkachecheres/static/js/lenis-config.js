const lenis = new Lenis({
    duration: .1, // Incrementa la duración para un scroll más fluido
    easing: (t) => t, // Easing lineal para un movimiento continuo
    direction: 'vertical',
    smooth: true,
    smoothTouch: false,
    touchMultiplier: 2
});

function raf(time) {
    lenis.raf(time);
    requestAnimationFrame(raf);
}
requestAnimationFrame(raf);

console.log("Scroll suave habilitado con Lenis");