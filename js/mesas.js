
// Datos de ejemplo para productos

const productos = [
    { nombre: "Producto A", precio: 10.00 },
    { nombre: "Producto B", precio: 15.00 },
    { nombre: "Producto C", precio: 20.00 },
];

let mesaSeleccionada = null;
let pedido = [];

// Seleccionar una mesa
// Datos de ejemplo para productos
const productos = [
    { nombre: "Producto A", precio: 10.00 },
    { nombre: "Producto B", precio: 15.00 },
    { nombre: "Producto C", precio: 20.00 },
];

let mesaSeleccionada = null;
let pedido = [];

// Seleccionar una mesa
document.querySelectorAll('.mesa').forEach(mesa => {
    mesa.addEventListener('click', () => {
        mesaSeleccionada = mesa.getAttribute('data-mesa');
        document.getElementById('mesa-seleccionada').textContent = mesaSeleccionada;
        document.querySelector('.pedido-section').style.display = 'block';
        actualizarPedido();
    });
});

// Agregar un producto al pedido
function agregarProducto() {
    const producto = productos[0]; /                      //Puedes-modificar-para-seleccionar-prodcto
    pedido.push({ ...producto, cantidad: 1 });
    actualizarPedido();
}

// Eliminar un producto del pedido
function eliminarProducto(index) {
    pedido.splice(index, 1);
    actualizarPedido();
}

// Actualizar la cantidad de un producto
function actualizarCantidad(index, cantidad) {
    pedido[index].cantidad = cantidad;
    actualizarPedido();
}

// Actualizar la tabla de pedidos
function actualizarPedido() {
    const tbody = document.getElementById('pedido-body');
    tbody.innerHTML = '';
    let total = 0;

    pedido.forEach((item, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${item.nombre}</td>
            <td>$${item.precio.toFixed(2)}</td>
            <td><input type="number" value="${item.cantidad}" onchange="actualizarCantidad(${index}, this.value)"></td>
            <td>$${(item.precio * item.cantidad).toFixed(2)}</td>
            <td><button onclick="eliminarProducto(${index})">Eliminar</button></td>
        `;
        tbody.appendChild(row);
        total += item.precio * item.cantidad;
    });

    document.getElementById('total-pedido').textContent = total.toFixed(2);
}

// Finalizar el pedido
function finalizarPedido() {
    const medioPago = document.getElementById('medio-pago').value;
    alert(`Pedido de la Mesa ${mesaSeleccionada} finalizado. Total: $${document.getElementById('total-pedido').textContent}. Medio de pago: ${medioPago}`);
    pedido = [];
    actualizarPedido();
}