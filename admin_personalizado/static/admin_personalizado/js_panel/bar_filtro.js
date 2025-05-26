// bar_filtros.js
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('filterModal');
    const openBtn = document.getElementById('openFilterModal');
    const closeBtn = document.querySelector('.close-button');
    const applyBtn = document.getElementById('applyFiltersButton');
    const resetBtn = document.getElementById('resetFiltersButton');

    // Función para aplicar la clase 'active-filter'
    function highlightActiveFilters() {
        const currentUrl = window.location.href.split('?')[0]; // URL base sin parámetros
        const currentParams = new URLSearchParams(window.location.search);

        document.querySelectorAll('.modal-filters-body a').forEach(link => {
            const linkUrl = link.href.split('?')[0];
            const linkParams = new URLSearchParams(link.href.split('?')[1] || '');

            const listItem = link.closest('li'); // Encuentra el <li> padre

            if (listItem) {
                listItem.classList.remove('active-filter');
            }

            let isLinkActive = true; 

            if (linkParams.toString()) {
                linkParams.forEach((linkValue, linkKey) => {
                    if (!currentParams.has(linkKey) || currentParams.get(linkKey) !== linkValue) {
                        isLinkActive = false;
                    }
                });

                currentParams.forEach((currentValue, currentKey) => {
                    if (currentKey !== 'q' && !linkParams.has(currentKey)) {
                        isLinkActive = false;
                    }
                });

            } else {
                let hasAnyFilterActive = false;
                currentParams.forEach((currentValue, currentKey) => {
                    if (currentKey !== 'q') {
                        hasAnyFilterActive = true;
                    }
                });
                isLinkActive = !hasAnyFilterActive;
            }

            if (isLinkActive && listItem) {
                listItem.classList.add('active-filter');
            }
        });
    }

    highlightActiveFilters();

    // Función para abrir el modal
    openBtn.addEventListener('click', function() {
        modal.classList.add('is-active'); // AÑADE LA CLASE is-active
        highlightActiveFilters();
    });

    // Función para cerrar el modal al hacer clic en la "x"
    closeBtn.addEventListener('click', function() {
        modal.classList.remove('is-active'); // QUITA LA CLASE is-active
    });

    // Función para cerrar el modal al hacer clic fuera del contenido del modal
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.classList.remove('is-active'); // QUITA LA CLASE is-active
        }
    });

    applyBtn.addEventListener('click', function() {
        modal.classList.remove('is-active'); // QUITA LA CLASE is-active
    });

    resetBtn.addEventListener('click', function() {
        modal.classList.remove('is-active'); // QUITA LA CLASE is-active
        window.location.href = window.location.pathname;
    });

    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            modal.classList.remove('is-active');
        }
    });
});