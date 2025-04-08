 // Script para la barra de navegación fija
 window.addEventListener('scroll', function() {
    const header = document.getElementById('navbar');
    if (window.scrollY > 100) {
        header.classList.add('scrolled');
    } else {
        header.classList.remove('scrolled');
    }
});

// Script para el carrusel de productos
document.addEventListener('DOMContentLoaded', function() {
    const cursor = document.getElementById('cursor');
    const leftArrow = document.getElementById('left-arrow');
    const rightArrow = document.getElementById('right-arrow');
    const cardItems = document.querySelectorAll('.card-item');

    // Configuración del desplazamiento
    const scrollAmount = 250;

    // Navegación con flechas
    leftArrow.addEventListener('click', function() {
        cursor.scrollBy({
            left: -scrollAmount,
            behavior: 'smooth'
        });
    });

    rightArrow.addEventListener('click', function() {
        cursor.scrollBy({
            left: scrollAmount,
            behavior: 'smooth'
        });
    });

    // Redirección al hacer clic en las tarjetas
    cardItems.forEach(card => {
        card.addEventListener('click', function() {
            const url = this.getAttribute('data-url');
            if (url) {
                window.location.href = url;
            }
        });
    });

    // Navegación con teclado para accesibilidad
    cursor.addEventListener('keydown', function(e) {
        if (e.key === 'ArrowLeft') {
            cursor.scrollBy({
                left: -scrollAmount,
                behavior: 'smooth'
            });
        } else if (e.key === 'ArrowRight') {
            cursor.scrollBy({
                left: scrollAmount,
                behavior: 'smooth'
            });
        }
    });
});