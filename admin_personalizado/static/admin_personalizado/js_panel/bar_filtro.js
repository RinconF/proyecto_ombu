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

            // Reinicia la clase activa para todos los filtros
            if (listItem) {
                listItem.classList.remove('active-filter');
            }

            let isLinkActive = true; // Asumimos que el enlace está activo inicialmente

            // Si el enlace tiene parámetros de filtro
            if (linkParams.toString()) {
                // El enlace es activo si todos sus parámetros existen en la URL actual Y sus valores coinciden
                linkParams.forEach((linkValue, linkKey) => {
                    if (!currentParams.has(linkKey) || currentParams.get(linkKey) !== linkValue) {
                        isLinkActive = false; // El parámetro no coincide, el enlace no está activo
                    }
                });

                // Además, verifica que la URL actual no tenga parámetros EXTRA (excepto 'q')
                // que no estén en el enlace. Esto asegura que no se resalte "activo: sí"
                // si la URL es "?is_active__exact=1&is_staff__exact=1".
                currentParams.forEach((currentValue, currentKey) => {
                    if (currentKey !== 'q' && !linkParams.has(currentKey)) {
                        isLinkActive = false; // Hay un parámetro extra, el enlace no es el ÚNICO filtro activo
                    }
                });

            } else { // Si el enlace es "Todo" (no tiene parámetros específicos)
                // El enlace "Todo" es activo si la URL actual NO tiene NINGÚN parámetro de filtro (excepto 'q')
                let hasAnyFilterActive = false;
                currentParams.forEach((currentValue, currentKey) => {
                    if (currentKey !== 'q') {
                        hasAnyFilterActive = true;
                    }
                });
                isLinkActive = !hasAnyFilterActive; // 'Todo' es activo si no hay otros filtros
            }

            if (isLinkActive && listItem) {
                listItem.classList.add('active-filter');
            }
        });
    }

    // --- Llama a la función al cargar la página para que los filtros activos se muestren ---
    highlightActiveFilters();

    // Función para abrir el modal
    openBtn.addEventListener('click', function() {
        modal.style.display = 'flex'; // Usamos 'flex' para centrar
        highlightActiveFilters(); // Llama de nuevo al abrir el modal por si la URL cambió
    });

    // Función para cerrar el modal al hacer clic en la "x"
    closeBtn.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    // Función para cerrar el modal al hacer clic fuera del contenido del modal
    window.addEventListener('click', function(event) {
        if (event.target == modal) {
            modal.style.display = 'none';
        }
    });

    // --- LÓGICA PARA LOS BOTONES DEL MODAL ---

    // Botón "Aplicar filtros"
    applyBtn.addEventListener('click', function() {
        modal.style.display = 'none'; // Solo cierra el modal. La navegación se hace con los <a>.
    });

    // Botón "Reiniciar filtros"
    resetBtn.addEventListener('click', function() {
        modal.style.display = 'none'; // Cierra el modal
        // Navega a la URL base de la lista (elimina todos los parámetros de filtro)
        window.location.href = window.location.pathname;
    });

    // Opcional: Cerrar modal si se presiona la tecla ESC
    document.addEventListener('keydown', function(event) {
        if (event.key === 'Escape') {
            modal.style.display = 'none';
        }
    });
});