        // Funciones para manejar los modales
        function openAddModal() {
            document.getElementById('addUserModal').style.display = 'block';
        }

        function closeAddModal() {
            document.getElementById('addUserModal').style.display = 'none';
            document.getElementById('addUserForm').reset();
        }

        function openEditModal(id, nombre, apellido, usuario, email, rol) {
            document.getElementById('edit_id').value = id;
            document.getElementById('edit_nombre').value = nombre;
            document.getElementById('edit_apellido').value = apellido;
            document.getElementById('edit_usuario').value = usuario;
            document.getElementById('edit_email').value = email;
            document.getElementById('edit_rol').value = rol;
            document.getElementById('editUserModal').style.display = 'block';
        }

        function closeEditModal() {
            document.getElementById('editUserModal').style.display = 'none';
            document.getElementById('editUserForm').reset();
        }

        // Función para cambiar el estado de un usuario (inhabilitar/habilitar)
        function cambiarEstado(id) {
            // En un caso real, aquí enviarías una solicitud al backend
            // Por ahora, simplemente mostramos un mensaje de confirmación
            if (confirm('¿Estás seguro de que deseas cambiar el estado de este usuario?')) {
                alert('Estado del usuario cambiado con éxito');
                // En un proyecto real, aquí actualizarías la UI o recargarías los datos
            }
        }

        // Manejo de formularios
        document.getElementById('addUserForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // Verificar que las contraseñas coincidan
            if (document.getElementById('password').value !== document.getElementById('confirm_password').value) {
                alert('Las contraseñas no coinciden');
                return;
            }
            // En un caso real, aquí enviarías los datos al backend
            alert('Usuario agregado con éxito');
            closeAddModal();
            // En un proyecto real, aquí actualizarías la tabla o recargarías los datos
        });

        document.getElementById('editUserForm').addEventListener('submit', function(e) {
            e.preventDefault();
            // En un caso real, aquí enviarías los datos al backend
            alert('Usuario actualizado con éxito');
            closeEditModal();
            // En un proyecto real, aquí actualizarías la tabla o recargarías los datos
        });