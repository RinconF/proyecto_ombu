function getCSRFToken() {
    let cookieValue = null;
    const name = 'csrftoken';
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function eliminarProducto(mesaId, index) {
    const clavePedidoMesa = `pedido_mesa_${mesaId}`;
    const pedidoActual = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];

    // Eliminar el producto en la posición 'index'
    pedidoActual.splice(index, 1);

    // Guardar los cambios en localStorage
    localStorage.setItem(clavePedidoMesa, JSON.stringify(pedidoActual));

    // **Vuelve a llamar a cargarPedido() para actualizar la vista**
    cargarPedido(mesaId);
}

document.querySelectorAll('.finalizar-pedido-btn').forEach(btn => {
    btn.addEventListener('click', () => {
        if (!mesaActivaId) {
            alert('Por favor, selecciona una mesa primero.');
            return;
        }
        // Obtener el medio de pago seleccionado
        const medioPagoSelect = document.querySelector('.medio-pago');
        const medioPago = medioPagoSelect ? medioPagoSelect.value : 'efectivo'; // Default si no se encuentra el select

        // AHORA PASAMOS EL MEDIO DE PAGO A LA FUNCIÓN
        finalizarPedido(mesaActivaId, medioPago); 
    });
});


// Seleccionar todas las mesas
const mesas = document.querySelectorAll('.mesa');
const pedidoSection = document.getElementById('pedido-section');
const mesaSeleccionadaText = document.getElementById('mesa-seleccionada');
const pedidoBody = document.getElementById('pedido-body');
const totalPedidoElement = document.getElementById('total-pedido');

let mesaActivaId = localStorage.getItem('mesaActivaId') || null;

mesas.forEach(mesa => {
    mesa.addEventListener('click', function() {
        const mesaId = mesa.getAttribute('data-mesa-id');  // Obtener ID de la mesa seleccionada
        mesaActivaId = mesaId;
        localStorage.setItem('mesaActivaId', mesaId); // Guardar el ID de la mesa activa

        
        // Si la mesa seleccionada ya está abierta, ocultar el pedido
        if (pedidoSection.style.display === 'block' && mesaSeleccionadaText.textContent === mesaId) {
            pedidoSection.style.display = 'none';
        } else {
           // Mostrar el pedido para la mesa seleccionada
           mesaSeleccionadaText.textContent = mesaId;
           pedidoSection.style.display = 'block';
           cargarPedido(mesaId); // Actualizar la vista del pedido para la mesa actual
        }
    });
// Seleccionar una mesa
});


// Función para cargar el pedido del localStorage y actualizar la vista
 function cargarPedido(mesaId) {
    const clavePedidoMesa = `pedido_mesa_${mesaId}`; // Clave única para cada mesa
    const pedido = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];

    const tbody = document.getElementById('pedido-body');
    tbody.innerHTML = ''; // Limpiar tabla antes de llenarla con los productos actuales
    let total = 0;
    let cantidadTotalProductos = 0;

    if (pedido.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5">No se realizaron compras.</td></tr>';
    } else {
        pedido.forEach((producto, index) => {
            console.log("Índice del producto:", index, "Producto:", producto.title);
            const row = document.createElement('tr');
            row.setAttribute('data-producto-id', producto.id);  // <-- añade el id
            row.innerHTML = `
                <td>${producto.title}</td>
                <td>$${producto.price.toFixed(2)}</td>
                <td><input class="cantidad-input" type="number" value="${producto.quantity}" min="1" /></td>
                <td>$${(producto.price * producto.quantity).toFixed(2)}</td>
                <td><button onclick="eliminarProducto('${mesaId}', ${index})">Eliminar</button></td>
            `;

            tbody.appendChild(row);

            // Sumar al total
            total += producto.price * producto.quantity;
            cantidadTotalProductos += parseInt(producto.quantity); // Sumar la cantidad de cada producto
        });
    }

    // Actualizar el total del pedido
    document.getElementById('total-pedido').textContent = `$${total.toFixed(2)}`;
    document.getElementById('cantidad-total-pedido').textContent = cantidadTotalProductos; // Mostrar la cantidad total
}


const agregarProductoBtn = document.getElementById('agregar-producto-btn');

if (agregarProductoBtn) {
    const bebidaCalienteUrl = agregarProductoBtn.dataset.url;

    agregarProductoBtn.addEventListener('click', function() {
        if (mesaActivaId) {
            window.location.href = `${bebidaCalienteUrl}?mesa=${mesaActivaId}`;
        } else {
            alert("Por favor, selecciona una mesa primero.");
        }
    });
}

function agregarAlPedido(mesaId, elemento) {
    const card = elemento.closest('.card');
    console.log("ID del producto:", card.dataset.id);
    const id = parseInt(card.dataset.id);
    const title = card.dataset.title;
    const price = parseFloat(card.dataset.price);
    const image = card.dataset.image;
    const options = card.dataset.options;

    const clavePedidoMesa = `pedido_mesa_${mesaId}`;
    let pedido = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];

    // Verificar si el producto ya está en el pedido
    const productoExistente = pedido.find(producto => producto.id === id && producto.options === options);
    if (productoExistente) {
        productoExistente.quantity += 1; // Sumar una unidad
    } else {
        pedido.push({
            id,
            title,
            price,
            image,
            options,
            quantity: 1
        });
    }

    localStorage.setItem(clavePedidoMesa, JSON.stringify(pedido));
    cargarPedido(mesaId); // Para refrescar la tabla de productos (si la tienes)
}





// Eliminar un producto específico del pedido






// Eliminar todo el pedido (vaciar el carrito)
function eliminarPedido(mesaId) {
    const clavePedidoMesa = `pedido_mesa_${mesaId}`;
    localStorage.setItem(clavePedidoMesa, JSON.stringify([]));
    cargarPedido(mesaId);
}

// funcion de finalizar pedido xdxd
function finalizarPedido(mesaId, medioPago) {
    const clavePedidoMesa = `pedido_mesa_${mesaId}`;
    const pedidoActual = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];

    if (pedidoActual.length === 0) {
        alert('El pedido está vacío. Agrega productos antes de finalizar.');
        return;
    }

    // Calcula el total del pedido
    // *** CAMBIO AQUI: USAR item.quantity y item.price ***
    const totalPedido = pedidoActual.reduce((sum, item) => sum + (item.quantity * item.price), 0); 

    // Recolectar solo los datos esenciales para la API
    const itemsParaEnviar = pedidoActual.map(item => ({
        producto_id: item.id,
        // *** CAMBIO AQUI: USAR item.quantity y item.price ***
        cantidad: item.quantity, 
        precio_unitario: item.price 
    }));

    // Datos a enviar al servidor
    const data = {
        mesa_id: mesaId,
        items: itemsParaEnviar,
        total: totalPedido,
        medio_pago: medioPago
    };

    fetch('/guardar_pedido/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify(data)
    })
    .then(response => {
        if (!response.ok) {
            return response.json().then(errorData => {
                throw new Error(errorData.error || 'Error desconocido al finalizar el pedido.');
            });
        }
        return response.json();
    })
    .then(data => {
        alert(data.message);
        localStorage.removeItem(clavePedidoMesa);
        cargarPedido(mesaId);
        actualizarEstadoMesas();
    })
    .catch(error => {
        console.error('Error al finalizar el pedido:', error);
        alert('Error al finalizar el pedido: ' + error.message);
    });
}


// Función para obtener cookie CSRF (útil para fetch con Django)


// -----------------------------------------------------------------------------------------------------------------------------------------------------------------------

function actualizarEstadoMesas() {
    const mesas = document.querySelectorAll('.mesa');
    
    mesas.forEach(mesa => {
        const mesaId = mesa.getAttribute('data-mesa-id');
        const clavePedidoMesa = `pedido_mesa_${mesaId}`;
        const pedido = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];
        
        // Agregar clase visual si hay pedidos
        if (pedido.length > 0) {
            mesa.classList.add('con-pedido');
            
            // Opcional: Mostrar contador de productos
            const cantidadTotal = pedido.reduce((total, item) => total + item.quantity, 0);
            const contadorElement = mesa.querySelector('.contador') || document.createElement('span');
            contadorElement.className = 'contador';
            contadorElement.textContent = cantidadTotal;
            mesa.appendChild(contadorElement);
        } else {
            mesa.classList.remove('con-pedido');
            const contador = mesa.querySelector('.contador');
            if (contador) {
                contador.remove();
            }
        }
    });
}
function agregarAlPedidoConMesaActiva(elemento) {
    const card = boton.closest('.card');
    const productoId = card.dataset.id;
    console.log('ID del producto:', productoId);
    if (!mesaActivaId) {
        alert("Selecciona una mesa primero");
        return;
    }
    agregarAlPedido(mesaActivaId, elemento);
}









function agregarProductoAlPedido(producto) {
    // producto debe ser un objeto con id, nombre, precio, cantidad, etc.
    const tbody = document.getElementById('pedido-body');

    const tr = document.createElement('tr');
    tr.setAttribute('data-producto-id', producto.id);  // <-- Aquí pones el ID

    tr.innerHTML = `
        <td>${producto.nombre}</td>
        <td>${producto.precio}</td>
        <td><input type="number" class="cantidad-input" value="${producto.cantidad}" min="0"></td>
        <td>${producto.precio * producto.cantidad}</td>
        <td><button class="eliminar-producto-btn">Eliminar</button></td>
    `;

    tbody.appendChild(tr);
}