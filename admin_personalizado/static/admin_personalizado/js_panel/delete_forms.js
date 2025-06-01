document.addEventListener('DOMContentLoaded', function() {
    console.log('delete_forms.js cargado. (Versión con clase is-active)'); // Mensaje actualizado

    const deleteModal = document.getElementById('delete-confirmation-modal');
    
    if (!deleteModal) {
        console.warn('El modal de confirmación de eliminación (#delete-confirmation-modal) no se encontró en la página. El script no funcionará para este modal.');
        return;
    }

    const closeDeleteModalButton = deleteModal.querySelector('.close-button');
    const confirmDeleteButton = deleteModal.querySelector('#confirm-delete-button');
    const cancelDeleteButton = deleteModal.querySelector('#cancel-delete-button');
    const objectNameToDeleteSpan = deleteModal.querySelector('#object-name-to-delete');

    let currentDeleteUrl = '';

    function openDeleteModal(objectName, deleteUrl) {
        if (objectNameToDeleteSpan) {
            objectNameToDeleteSpan.textContent = objectName;
        }
        currentDeleteUrl = deleteUrl;
        deleteModal.classList.add('is-active'); // CAMBIO AQUÍ: Añade la clase 'is-active'
        document.body.classList.add('modal-open');
    }

    function closeDeleteModal() {
        deleteModal.classList.remove('is-active'); // CAMBIO AQUÍ: Quita la clase 'is-active'
        document.body.classList.remove('modal-open');
        currentDeleteUrl = '';
    }

    if (closeDeleteModalButton) {
        closeDeleteModalButton.addEventListener('click', closeDeleteModal);
    }
    if (cancelDeleteButton) {
        cancelDeleteButton.addEventListener('click', closeDeleteModal);
    }
    window.addEventListener('click', function(event) {
        if (event.target === deleteModal) {
            closeDeleteModal();
        }
    });

    if (confirmDeleteButton) {
        confirmDeleteButton.addEventListener('click', function(event) {
            event.preventDefault();
            
            if (currentDeleteUrl) {
                const csrftoken = getCookie('csrftoken');

                const form = document.createElement('form');
                form.method = 'POST';
                form.action = currentDeleteUrl;
                
                const csrfInput = document.createElement('input');
                csrfInput.type = 'hidden';
                csrfInput.name = 'csrfmiddlewaretoken';
                csrfInput.value = csrftoken;
                form.appendChild(csrfInput);

                const postInput = document.createElement('input');
                postInput.type = 'hidden';
                postInput.name = 'post';
                postInput.value = 'yes';
                form.appendChild(postInput);

                document.body.appendChild(form);
                form.submit();
            } else {
                console.error('No se pudo determinar la URL de eliminación.');
                closeDeleteModal();
            }
        });
    }

    document.querySelectorAll('a.action-delete, a.custom-delete-button').forEach(button => {
        button.addEventListener('click', function(event) {
            event.preventDefault();

            const deleteUrl = this.dataset.deleteUrl || this.href;
            let objectName = this.dataset.objectName || 'este elemento';

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