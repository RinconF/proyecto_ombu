// Credenciales únicas
const usuarioCorrecto = "admin";
const contrasenaCorrecta = "1234";

// Obtener el formulario y el mensaje de error
const loginForm = document.getElementById('loginForm');
const errorMessage = document.getElementById('errorMessage');
// Ocultar el mensaje de error inicialmente
errorMessage.style.display = 'none';

// Manejar el envío del formulario
loginForm.addEventListener('submit', function(event) {
  event.preventDefault(); // Evitar que el formulario se envíe
  // Obtener los valores ingresados
  const username = document.getElementById('username').value.trim();
  const password = document.getElementById('password').value.trim();
  
  // Validar si los campos están vacíos
  if (username === "" || password === "") {
      errorMessage.textContent = "Por favor, completa todos los campos.";
      errorMessage.style.display = 'block';
      return; // Detener la ejecución
  }
  
  // Validar las credenciales
  if (username === usuarioCorrecto && password === contrasenaCorrecta) {
      // Mostrar mensaje de éxito
      alert("¡Ingreso exitoso! Bienvenido al sistema.");
      // Redirigir a la página específica después del alert
      window.location.href = "admin_principal.html";
  } else {
      // Mostrar mensaje de error
      errorMessage.textContent = "Usuario o contraseña incorrectos.";
      errorMessage.style.display = 'block';
  }
});

// Manejar el clic en "¿Olvidaste tu contraseña?"
document.getElementById('forgotPassword').addEventListener('click', function() {
  alert("Por favor, contacta al soporte técnico.");
});

// Alternar entre login y registro
const container = document.querySelector('.container');
const registerBtn = document.querySelector('.register-btn');
const loginBtn = document.querySelector('.login-btn');

registerBtn.addEventListener('click', () => {
  container.classList.add('active');
});

loginBtn.addEventListener('click', () => {
  container.classList.remove('active');
});