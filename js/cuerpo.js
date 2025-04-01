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