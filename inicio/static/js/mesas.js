// Seleccionar todas las mesas
const mesas = document.querySelectorAll('.mesa');
const pedidoSection = document.getElementById('pedido-section');
const mesaSeleccionadaText = document.getElementById('mesa-seleccionada');
const pedidoBody = document.getElementById('pedido-body');
const totalPedidoElement = document.getElementById('total-pedido');

let mesaActivaId = localStorage.getItem('mesaActivaId') || null;

mesas.forEach(mesa => {
    mesa.addEventListener('click', function() {
        const mesaId = mesa.getAttribute('data-mesa');  // Obtener ID de la mesa seleccionada
        mesaActivaId = mesaId; // Guardar el ID de la mesa activa

        
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
    //        window.location.href = `/pages/menu_mesero/bebidas_frias.html?mesa=${mesaId}`; guardar esta linea por si algo//
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
            row.innerHTML = `
                <td>${producto.title}</td>
                <td>$${producto.price.toFixed(2)}</td>
                <td><span>${producto.quantity}</span></td>
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
    agregarProductoBtn.addEventListener('click', function() {
        if (mesaActivaId) {
            window.location.href = `/pages/menu_mesero/bebidas_calientes.html?mesa=${mesaActivaId}`;
        } else {
            alert("Por favor, selecciona una mesa primero.");
        }
    });
}




// Eliminar un producto específico del pedido
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






// Eliminar todo el pedido (vaciar el carrito)
function eliminarPedido(mesaId) {
    const clavePedidoMesa = `pedido_mesa_${mesaId}`;
    localStorage.setItem(clavePedidoMesa, JSON.stringify([]));
    cargarPedido(mesaId);
}

// Finalizar el pedido
function finalizarPedido() {
    const mesaId = document.getElementById('mesa-seleccionada').textContent;
    const medioPago = document.getElementById('medio-pago').value;
    const totalPedido = document.getElementById('total-pedido').textContent;

    alert(`Pedido de la Mesa ${mesaId} finalizado. Total: ${totalPedido}. Medio de pago: ${medioPago}`);

    // Limpiar el pedido de la mesa actual en localStorage
    eliminarPedido(mesaId);
}


function actualizarEstadoMesas() {
    const mesas = document.querySelectorAll('.mesa');
    
    mesas.forEach(mesa => {
        const mesaId = mesa.getAttribute('data-mesa');
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