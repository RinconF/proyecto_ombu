// Seleccionar elementos
const cursor = document.getElementById('cursor');
const leftArrow = document.getElementById('left-arrow');
const rightArrow = document.getElementById('right-arrow');
const cards = document.querySelectorAll('.card-item');

// Función para calcular el desplazamiento dinámicamente
function getScrollAmount() {
    const card = document.querySelector('.card-item');
    const cardWidth = card ? card.offsetWidth : 180;
    const gap = 10;
    return cardWidth + gap;
}

// Desplazamiento a la izquierda
leftArrow.addEventListener('click', () => {
    const scrollAmount = getScrollAmount();
    cursor.scrollBy({ left: -scrollAmount, behavior: 'smooth' });
});

// Desplazamiento a la derecha
rightArrow.addEventListener('click', () => {
    const scrollAmount = getScrollAmount();
    cursor.scrollBy({ left: scrollAmount, behavior: 'smooth' });
});

// Redirigir al hacer clic en una tarjeta
cards.forEach(card => {
    card.addEventListener('click', () => {
        const url = card.getAttribute('data-url');
        if (url) {
            window.location.href = url; // Redirige a la URL especificada
        }
    });
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
});