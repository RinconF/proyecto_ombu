// Script animacion productos
const flavors = [
  {
    name: ["la", "tte"],
    color: "rgba(74, 145, 226, 0.36)",
    image:
      "https://raw.githubusercontent.com/nidal1111/storage/master/assets/milkshake_banana.png",
  },
  {
    name: ["Maple", "Peanut"],
    color: "rgba(233, 75, 75, 0.24)",
    image:
      "https://raw.githubusercontent.com/nidal1111/storage/master/assets/milkShake_caffe%CC%80.png",
  },
  {
    name: ["Cacao", "Coconut"],
    color: "rgba(244, 208, 63, 0.22)",
    image:
      "https://raw.githubusercontent.com/nidal1111/storage/master/assets/milkShake_fragole.png",
  },
  {
    name: ["Berry", "Blend"],
    color: "rgba(141, 68, 173, 0.2)",
    image:
      "https://raw.githubusercontent.com/nidal1111/storage/master/assets/milkshake_banana.png",
  }
];

let currentIndex = 0;
let isAnimating = false;

const container = document.querySelector(".slider-container");
const overlay = document.querySelector(".color-overlay");
const firstWord = document.querySelector(".first-word");
const secondWord = document.querySelector(".second-word");
const imageElement = document.querySelector(".milkshake-image");
const nutritionValues = document.querySelectorAll(".nutrition-value");
const dots = document.querySelectorAll(".control-dot");

function initSlider() {
  const currentFlavor = flavors[currentIndex];
  container.style.background = currentFlavor.color;
  firstWord.textContent = currentFlavor.name[0];
  secondWord.textContent = currentFlavor.name[1];
  imageElement.src = currentFlavor.image;
}

function morphWords(fromWords, toWords, onComplete) {
  const [fromFirst, fromSecond] = fromWords;
  const [toFirst, toSecond] = toWords;

  firstWord.style.transform = "translateX(0)";
  secondWord.style.transform = "translateX(0)";

  const maxMoveDistance = 20;

  let step = 0;
  const totalSteps = 40;

  function nextFrame() {
    if (step < totalSteps) {
      const progress = step / (totalSteps - 1);
      const easeProgress = progress * progress * progress;

      const moveDistance = maxMoveDistance * easeProgress;
      firstWord.style.transform = `translateX(${moveDistance}px)`;
      secondWord.style.transform = `translateX(-${moveDistance}px)`;

      const firstCharsToShow = Math.max(
        0,
        Math.ceil(fromFirst.length * (1 - easeProgress))
      );
      const secondCharsToShow = Math.max(
        0,
        Math.ceil(fromSecond.length * (1 - easeProgress))
      );

      const currentFirst = fromFirst.substring(0, firstCharsToShow);
      const currentSecond = fromSecond.substring(
        fromSecond.length - secondCharsToShow
      );

      if (currentFirst !== firstWord.textContent) {
        firstWord.textContent = currentFirst;
      }
      if (currentSecond !== secondWord.textContent) {
        secondWord.textContent = currentSecond;
      }

      step++;
      requestAnimationFrame(nextFrame);
    } else {
      setTimeout(() => {
        let expandStep = 0;
        const expandSteps = 40;

        function expandFrame() {
          const expandProgress = expandStep / (expandSteps - 1);
          const easeExpandProgress =
            expandProgress * expandProgress * (3 - 2 * expandProgress);

          const returnDistance = maxMoveDistance * (1 - easeExpandProgress);
          firstWord.style.transform = `translateX(${returnDistance}px)`;
          secondWord.style.transform = `translateX(-${returnDistance}px)`;

          const firstCharsToShow = Math.ceil(
            toFirst.length * easeExpandProgress
          );
          const secondCharsToShow = Math.ceil(
            toSecond.length * easeExpandProgress
          );

          const currentFirst = toFirst.substring(0, firstCharsToShow);
          const currentSecond = toSecond.substring(
            toSecond.length - secondCharsToShow
          );

          if (currentFirst !== firstWord.textContent) {
            firstWord.textContent = currentFirst;
          }
          if (currentSecond !== secondWord.textContent) {
            secondWord.textContent = currentSecond;
          }

          if (expandStep < expandSteps) {
            expandStep++;
            requestAnimationFrame(expandFrame);
          } else {
            firstWord.style.transform = "translateX(0)";
            secondWord.style.transform = "translateX(0)";
            firstWord.textContent = toFirst;
            secondWord.textContent = toSecond;
            if (onComplete) onComplete();
          }
        }

        expandFrame();
      }, 100);
    }
  }

  nextFrame();
}

function animateNutritionValues(newValues) {
  nutritionValues.forEach((value, index) => {
    setTimeout(() => {
      value.style.opacity = "0";
      setTimeout(() => {
        value.textContent = newValues[index];
        value.style.opacity = "1";
      }, 150);
    }, index * 80);
  });
}

function changeSlide(newIndex) {
  if (newIndex === currentIndex || isAnimating) return;

  isAnimating = true;
  const currentFlavor = flavors[currentIndex];
  const newFlavor = flavors[newIndex];

  overlay.style.background = newFlavor.color;
  overlay.classList.add("slide-down");

  setTimeout(() => {
    morphWords(currentFlavor.name, newFlavor.name);
    animateNutritionValues(newFlavor.nutrition);

    setTimeout(() => {
      imageElement.src = newFlavor.image;
      imageElement.style.opacity = "0";

      setTimeout(() => {
        container.style.background = newFlavor.color;
        overlay.classList.remove("slide-down");
        overlay.style.transform = "translateY(-100%)";

        setTimeout(() => {
          imageElement.style.opacity = "1";
          overlay.style.transform = "";
          isAnimating = false;
        }, 300);
      }, 100);
    }, 400);
  }, 0);

  dots[currentIndex].classList.remove("active");
  dots[newIndex].classList.add("active");
  currentIndex = newIndex;
}

function autoSlide() {
  if (!isAnimating) {
    const nextIndex = (currentIndex + 1) % flavors.length;
    changeSlide(nextIndex);
  }
}

dots.forEach((dot, index) => {
  dot.addEventListener("click", () => changeSlide(index));
});

initSlider();
setInterval(autoSlide, 4000);


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



document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const mainMenu = document.getElementById('mainMenu');
    
    // Toggle menu cuando se hace clic en el botón hamburguesa
    menuToggle.addEventListener('click', function() {
      mainMenu.classList.toggle('active');
    });
    
    // Cerrar menú cuando se hace clic en un enlace
    const menuLinks = document.querySelectorAll('.link');
    menuLinks.forEach(link => {
      link.addEventListener('click', function() {
        if (window.innerWidth <= 600) {
          mainMenu.classList.remove('active');
        }
      });
    });
    
    // Cerrar menú si se hace clic fuera de él
    document.addEventListener('click', function(event) {
      const isClickInsideMenu = mainMenu.contains(event.target);
      const isClickOnToggle = menuToggle.contains(event.target);
      
      if (!isClickInsideMenu && !isClickOnToggle && mainMenu.classList.contains('active')) {
        mainMenu.classList.remove('active');
      }
    });
  });


// JavaScript para el menú desplegable en escritorio (para que aparezca y desaparezca al subir y bajar el scroll)
document.addEventListener("DOMContentLoaded", () => {
    const menuContainer = document.querySelector(".menu-container");
    const main = document.querySelector("main");
    let lastScrollTop = 0;

    function handleScroll() {
        // Verifica el ancho de la pantalla para aplicar solo en escritorio
        if (window.innerWidth <= 767) {
            menuContainer.classList.remove("menu-fixed", "menu-hidden");
            return;
        }

        let currentScrollTop = main.scrollTop || document.documentElement.scrollTop;

        if (currentScrollTop > 150) {
            menuContainer.classList.add("menu-fixed");
        } else {
            menuContainer.classList.remove("menu-fixed");
        }

        if (currentScrollTop > lastScrollTop) {
            menuContainer.classList.add("menu-hidden"); // Oculta al bajar
        } else {
            menuContainer.classList.remove("menu-hidden"); // Muestra al subir
        }

        lastScrollTop = currentScrollTop;
    }

    // Agrega el evento de scroll al `main` en lugar de `window`
    window.addEventListener("scroll", handleScroll);
});

// loader

window.addEventListener('load', function () {
  setTimeout(() => {
    document.getElementById('loader').style.opacity = '0';
    document.getElementById('loader').style.visibility = 'hidden';
    document.querySelector('.contenido').style.visibility = 'visible';
  }, 1000); // 1000 ms = 1 segundo
});


// buscador


