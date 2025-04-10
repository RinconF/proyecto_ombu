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
<<<<<<< HEAD
});

//reduccion de la barra de navegacion

// window.onscroll = function() {
//     reduceNavbar();
// };

// function reduceNavbar() {
//     const navbar = document.getElementById("navbar");
//     if (window.scrollY > 50) {  // Cuando el desplazamiento es mayor a 50px
//         navbar.classList.add("scrolled"); // Añadir la clase para reducir el header
//     } else {
//         navbar.classList.remove("scrolled"); // Quitar la clase cuando el scroll vuelve al principio
//     }
// }


// Obtener el elemento del encabezado
const navbar = document.getElementById('navbar');

// Función para reducir el encabezado al hacer scroll
window.onscroll = function() {
    if (window.scrollY > 50) {
        navbar.classList.add('shrink');  // Agrega la clase 'shrink' si el scroll es mayor a 50px
    } else {
        navbar.classList.remove('shrink');  // Elimina la clase 'shrink' cuando el scroll es menor a 50px
    }
};

// Función para mostrar/ocultar el menú al hacer clic en el botón de hamburguesa
const menuToggle = document.getElementById('menuToggle');
const mainMenu = document.getElementById('mainMenu');

menuToggle.addEventListener('click', () => {
    mainMenu.classList.toggle('show');
=======
>>>>>>> 0226fac63b69a6d2af0a5fe5d5837d7a8f32c0a3
});