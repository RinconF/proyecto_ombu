document.addEventListener('DOMContentLoaded', function() {
    console.log('delete_forms.js cargado. (Versión para modal pre-existente)');

    const deleteModal = document.getElementById('delete-confirmation-modal');
    // Asegúrate de que el modal existe antes de intentar acceder a sus elementos internos
    if (!deleteModal) {
        console.warn('El modal de confirmación de eliminación (#delete-confirmation-modal) no se encontró en la página. El script no funcionará para este modal.');
        return; // Detiene la ejecución si el modal no se encuentra
    }

    const closeDeleteModalButton = deleteModal.querySelector('.close-button');
    const confirmDeleteButton = deleteModal.querySelector('#confirm-delete-button');
    const cancelDeleteButton = deleteModal.querySelector('#cancel-delete-button');
    const objectNameToDeleteSpan = deleteModal.querySelector('#object-name-to-delete');

    let currentDeleteUrl = ''; // Variable para almacenar la URL de eliminación

    function openDeleteModal(objectName, deleteUrl) {
        if (objectNameToDeleteSpan) {
            objectNameToDeleteSpan.textContent = objectName;
        }
        currentDeleteUrl = deleteUrl;
        deleteModal.style.display = 'flex'; // Usamos flex para centrar
        document.body.classList.add('modal-open'); // Previene scroll del body
    }

    function closeDeleteModal() {
        deleteModal.style.display = 'none';
        document.body.classList.remove('modal-open');
        currentDeleteUrl = ''; // Limpiar la URL al cerrar
    }

    // Event listeners para cerrar el modal
    if (closeDeleteModalButton) {
        closeDeleteModalButton.addEventListener('click', closeDeleteModal);
    }
    if (cancelDeleteButton) {
        cancelDeleteButton.addEventListener('click', closeDeleteModal);
    }
    // Cierra el modal al hacer clic fuera del contenido del modal
    window.addEventListener('click', function(event) {
        if (event.target === deleteModal) { // Asegúrate de que el clic fue directamente en el fondo del modal
            closeDeleteModal();
        }
    });

    // Event listener para el botón de CONFIRMAR eliminación dentro del modal
    if (confirmDeleteButton) {
        confirmDeleteButton.addEventListener('click', function(event) {
            event.preventDefault(); // Prevenir la acción por defecto del botón
            
            if (currentDeleteUrl) {
                // Obtener el token CSRF para peticiones POST en Django
                const csrftoken = getCookie('csrftoken');

                // Crear un formulario temporal y enviarlo para simular la eliminación POST
                const form = document.createElement('form');
                form.method = 'POST';
                form.action = currentDeleteUrl; // La URL de eliminación
                
                // Añadir el token CSRF al formulario
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrftoken;
                form.appendChild(csrfInput);

                // Añadir un input oculto para '_post' si la vista de eliminación lo requiere (Django admin lo hace)
                const postInput = document.createElement('input');
                postInput.type = 'hidden';
                postInput.name = 'post'; // O '_post' dependiendo de la versión de Django o cómo maneje la vista
                postInput.value = 'yes';
                form.appendChild(postInput);

                // Añadir el formulario al body y enviarlo
                document.body.appendChild(form);
                form.submit();
            } else {
                console.error('No se pudo determinar la URL de eliminación.');
                closeDeleteModal();
            }
        });
    }

    // Intercepta los clics en los botones/enlaces de "Eliminar" en la página
    // Asegúrate de que este selector coincide con tus botones de eliminar
    document.querySelectorAll('a.action-delete, a.custom-delete-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault(); // ¡Esto es CRUCIAL! Detiene la navegación por defecto

            const deleteUrl = this.dataset.deleteUrl || this.href;
            let objectName = this.dataset.objectName || 'este elemento';

            // Lógica adicional para obtener el objectName de la tabla (solo relevante para changelist si no tiene data-object-name)
            // Esto es si el botón está en la lista (changelist) y no tiene un data-object-name explícito
            if (!this.dataset.objectName && this.classList.contains('action-delete')) {
                let currentRow = this.closest('tr');
                if (currentRow) {
                    const objectLink = currentRow.querySelector('th a');
                    if (objectLink) {
                        objectName = objectLink.textContent.trim();
                    } else {
                        const firstDataCell = currentRow.querySelector('td:not(.action-checkbox)');
                        if (firstDataCell) {
                            objectName = firstDataCell.textContent.trim();
                        }
                    }
                }
            }
            openDeleteModal(objectName, deleteUrl);
        });
    });

    // Función para obtener el token CSRF (necesario para peticiones POST en Django)
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});