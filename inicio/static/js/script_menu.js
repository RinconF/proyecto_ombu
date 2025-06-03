document.addEventListener("DOMContentLoaded", () => {
    // === Variables globales (centralizadas) ===
    let cart = JSON.parse(localStorage.getItem('cart')) || []; // Recuperar carrito desde localStorage
    let cartOpen = false;
    let currentProductData = {
        card: null,
        options: {},
        currentPrice: 0,
        currentPriceDisplay: '',
        basePrice: 0
    };

    // Obtener el mesaId y mesaNumero de la URL al cargar la página
    // Primero intentamos de la URL, si no, del localStorage (que mesas.js debería haber seteado)
    let mesaIdActiva = getUrlParameter('mesa_id') || localStorage.getItem('mesaActivaId');
    let mesaNumeroActivo = getUrlParameter('mesa_numero') || localStorage.getItem('mesaActivaNumero');

    // Referencias a elementos del DOM
    const cards = document.querySelectorAll(".card");
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const modalImage = document.getElementById("modal-image");
    const modalSelect = document.getElementById("modal-select");
    const closeModal = document.querySelector(".close");

    const cartIcon = document.getElementById('cart-icon');
    const cartContainer = document.getElementById('cart-container');
    const closeCartBtn = document.getElementById('close-cart');
    const cartItems = document.getElementById('cart-items');
    const cartTotalAmount = document.getElementById('cart-total-amount');
    const cartCount = document.getElementById('cart-count');
    const checkoutButton = document.getElementById('checkout-button');
    const emptyCartButton = document.getElementById('empty-cart');

    const overlay = document.createElement('div');
    overlay.className = 'cart-overlay';
    document.body.appendChild(overlay);

    // Actualizar el texto del botón de finalizar compra si hay una mesa activa
    if (checkoutButton && mesaNumeroActivo) {
        checkoutButton.textContent = "Finalizar compra en mesa " + mesaNumeroActivo;
    } else if (checkoutButton) {
        checkoutButton.textContent = "Finalizar compra"; // O un texto predeterminado
    }

    // === Funciones de Utilidad ===

    // Función para obtener un parámetro de la URL
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        const results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // Función para actualizar el carrito en localStorage
    function updateCartStorage() {
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    // Función para cerrar el carrito
    function closeCart() {
        cartContainer.classList.remove('open');
        overlay.style.display = 'none';
        cartOpen = false;
    }

    // === Inicialización de Navegación (Más limpia y menos agresiva) ===
    // Esta lógica ahora se encarga de que los enlaces del menú principal
    // (si los tienes con una clase específica, o si están en un contenedor específico)
    // lleven el `mesa_id` y `mesa_numero` si existen.

    // Primero, obtener los elementos del menú que deberían llevar el ID de mesa
    // Suponiendo que tus enlaces de categoría tienen la clase 'menu-category-link'
    const menuLinks = document.querySelectorAll('.main-nav a'); // Ajusta este selector si tus enlaces de categoría tienen otra clase o estructura
    menuLinks.forEach(link => {
        const originalHref = link.getAttribute('href');
        if (originalHref && !originalHref.startsWith('#') && !originalHref.includes('?')) { // Solo enlaces internos sin parámetros
            if (mesaIdActiva && mesaNumeroActivo) {
                link.href = `${originalHref}?mesa_id=${mesaIdActiva}&mesa_numero=${mesaNumeroActivo}`;
            }
        }
    });

    // === Gestión del Modal de Productos ===

    // Crear elemento para mostrar el precio en el modal
    const modalPrice = document.createElement('div');
    modalPrice.className = 'modal-price';
    modalPrice.style.fontWeight = 'bold';
    modalPrice.style.fontSize = '1.2rem';
    modalPrice.style.margin = '10px 0';
    modalPrice.style.color = '#20AB47';

    // Añadir el botón "Agregar al carrito" al modal
    let modalAddToCartBtn = document.getElementById("modal-add-to-cart");
    if (!modalAddToCartBtn) {
        modalAddToCartBtn = document.createElement('button');
        modalAddToCartBtn.id = 'modal-add-to-cart';
        modalAddToCartBtn.textContent = 'Agregar al carrito';
        modalAddToCartBtn.style.marginTop = '15px';
        modalAddToCartBtn.style.width = '100%';
        modalAddToCartBtn.classList.add('button'); // Añade tu clase de botón si tienes una
    }

    // Añadir el elemento de precio al modal después del título
    const modalInfo = modal.querySelector('.modal-info');
    if (modalInfo && modalTitle) {
        modalInfo.insertBefore(modalPrice, modalTitle.nextSibling);
        // Asegurarse de que el botón de agregar al carrito esté al final
        if (!document.getElementById("modal-add-to-cart")) { // Doble verificación para evitar duplicados
            modalInfo.appendChild(modalAddToCartBtn);
        }
    }

    // Añadir botones "Agregar al carrito" a todas las tarjetas si no existen
    document.querySelectorAll('.footer-card').forEach(footer => {
        if (!footer.querySelector('.add-to-cart-btn')) {
            const addButton = document.createElement('button');
            addButton.className = 'add-to-cart-btn';
            addButton.innerHTML = '+';
            footer.appendChild(addButton);

            // Ajustar el estilo del botón "Ver más"
            const verMasBtn = footer.querySelector('button:not(.add-to-cart-btn)');
            if (verMasBtn) {
                verMasBtn.style.marginRight = 'auto';
            }
        }
    });

    // Funcionalidad del modal al hacer clic en la tarjeta
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            // No abrir el modal si se hizo clic en el botón "Agregar al carrito"
            if (e.target.classList.contains('add-to-cart-btn')) {
                return;
            }

            // Obtener datos del producto
            const title = card.getAttribute('data-title') || card.querySelector('.main-card > span').textContent;
            const imgSrc = card.getAttribute('data-image') || card.querySelector('img').src;

            // Obtener precio base de la tarjeta
            const priceElement = card.querySelector('.footer-card > span');
            const basePrice = priceElement ? priceElement.textContent : '$0';
            const basePriceValue = parseFloat(basePrice.replace(/[^0-9.-]+/g, '')) || 0; // Para manejar monedas como '$1.234,56'

            // Guardar referencia a la tarjeta actual y precio base
            currentProductData.card = card;
            currentProductData.basePrice = basePriceValue;
            currentProductData.currentPrice = basePriceValue;
            currentProductData.currentPriceDisplay = basePrice;

            // Inicializar opciones con precio predeterminado
            currentProductData.options = {
                'Regular': {
                    price: basePriceValue,
                    priceDisplay: basePrice
                }
            };

            // Actualizar el contenido del modal
            modalTitle.textContent = title;
            modalImage.src = imgSrc;
            modalImage.alt = title;
            modalPrice.textContent = basePrice;

            // Manejar opciones de precios
            modalSelect.innerHTML = '';
            try {
                const options = card.getAttribute('data-options');
                if (options) {
                    const optionsArray = options.split(',').map(opt => opt.trim()).filter(opt => opt.length > 0);
                    optionsArray.forEach(option => {
                        const optionElement = document.createElement('option');
                        optionElement.value = option;
                        optionElement.textContent = option;
                        modalSelect.appendChild(optionElement);

                        // Establecer el mismo precio para todas las opciones (ajusta si tienes precios por opción)
                        currentProductData.options[option] = {
                            price: basePriceValue,
                            priceDisplay: basePrice
                        };
                    });
                } else {
                    // Opción predeterminada si no hay data-options
                    const optionElement = document.createElement('option');
                    optionElement.value = "Regular";
                    optionElement.textContent = "Regular";
                    modalSelect.appendChild(optionElement);
                }
            } catch (e) {
                console.error("Error al analizar opciones:", e);
                // Opción alternativa
                const optionElement = document.createElement('option');
                optionElement.value = "Regular";
                optionElement.textContent = "Regular";
                modalSelect.appendChild(optionElement);
            }

            // Mostrar el modal
            modal.style.display = "flex";
        });
    });

    // Evento de cambio de opción en el modal
    modalSelect.addEventListener('change', function() {
        const selectedOption = this.value;
        if (currentProductData.options && currentProductData.options[selectedOption]) {
            // Actualizar el precio mostrado con el precio para esta opción
            modalPrice.textContent = currentProductData.options[selectedOption].priceDisplay;
            currentProductData.currentPrice = currentProductData.options[selectedOption].price;
            currentProductData.currentPriceDisplay = currentProductData.options[selectedOption].priceDisplay;
        }
    });

    // Cerrar el modal
    closeModal.addEventListener('click', () => {
        modal.style.display = "none";
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    });

    // === Carrito de compras - Abrir y cerrar ===
    cartIcon.addEventListener('click', function() {
        cartContainer.classList.add('open');
        overlay.style.display = 'block';
        cartOpen = true;
    });

    closeCartBtn.addEventListener('click', closeCart);
    overlay.addEventListener('click', closeCart);


    // === Lógica de agregar al carrito ===

    // Agregar al carrito desde las tarjetas (botón '+')
    document.querySelectorAll('.add-to-cart-btn').forEach((button) => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Evitar que se abra el modal

            const card = this.closest('.card');
            const imgSrc = card.querySelector('img').src;
            const title = card.querySelector('.main-card > span').textContent;
            const priceElement = card.querySelector('.footer-card > span');
            const price = priceElement ? priceElement.textContent : '$0';
            const priceValue = parseFloat(price.replace(/[^0-9.-]+/g, '')) || 0; // Asegura que el precio sea numérico
            const productId = card.dataset.id;
            const options = card.dataset.options || 'Regular'; // Obtener opciones directamente de la tarjeta

            // Verificar si el artículo ya está en el carrito
            const existingItemIndex = cart.findIndex(item => item.id == productId && item.option === 'Regular'); // Asumimos 'Regular' para botón directo

            if (existingItemIndex !== -1) {
                cart[existingItemIndex].quantity += 1;
            } else {
                const cartItem = {
                    id: productId,
                    imgSrc,
                    title,
                    price: priceValue,
                    priceDisplay: price,
                    quantity: 1,
                    option: 'Regular' // Opción predeterminada para el botón '+'
                };
                cart.push(cartItem);
            }
            updateCartDisplay();

            // Animación para el icono del carrito
            cartCount.style.transform = 'scale(1.3)';
            setTimeout(() => {
                cartCount.style.transform = 'scale(1)';
            }, 300);
        });
    });

    // Agregar al carrito desde el modal (botón "Agregar al carrito")
    modalAddToCartBtn.addEventListener('click', function() {
        const title = modalTitle.textContent;
        const imgSrc = modalImage.src;
        const productId = currentProductData.card.dataset.id;

        // Obtener opción seleccionada del modal
        let option = 'Regular';
        if (modalSelect && modalSelect.value) {
            option = modalSelect.value;
        }

        // Usar el precio actual del producto (que se actualiza con la selección del modal)
        const price = currentProductData.currentPrice;
        const priceDisplay = currentProductData.currentPriceDisplay;

        if (price > 0) {
            // Verificar si el artículo con el mismo ID de producto y opción está en el carrito
            const existingItemIndex = cart.findIndex(item =>
                item.id == productId && item.option === option
            );

            if (existingItemIndex !== -1) {
                cart[existingItemIndex].quantity += 1;
            } else {
                const cartItem = {
                    id: productId,
                    imgSrc,
                    title,
                    price: price,
                    priceDisplay: priceDisplay,
                    quantity: 1,
                    option
                };
                cart.push(cartItem);
            }

            updateCartDisplay();

            // Cerrar modal
            modal.style.display = 'none';

            // Animación y abrir carrito (opcional, puedes comentar si no quieres que se abra al agregar desde el modal)
            cartCount.style.transform = 'scale(1.3)';
            setTimeout(() => {
                cartCount.style.transform = 'scale(1)';
                cartContainer.classList.add('open');
                overlay.style.display = 'block';
                cartOpen = true;
            }, 300);
        }
    });

    // === Finalizar compra (Envía al localStorage de la mesa activa) ===
    checkoutButton.addEventListener('click', function() {
        if (cart.length === 0) {
            alert('Su carrito está vacío');
            return;
        }

        // Usar mesaIdActiva y mesaNumeroActivo que se obtienen al inicio del script
        if (!mesaIdActiva || !mesaNumeroActivo) {
            alert('No se pudo identificar la mesa activa. Por favor, asegúrese de haber seleccionado una mesa.');
            return;
        }

        const clavePedidoMesa = `pedido_mesa_${mesaIdActiva}`;

        // Obtener pedidos existentes para esta mesa del localStorage
        const pedidosExistentes = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];

        // Combinar con los nuevos productos del carrito, manejando duplicados por ID de producto y opción
        cart.forEach(newItem => {
            const existingItem = pedidosExistentes.find(
                p => p.id == newItem.id && p.option === newItem.option
            );
            if (existingItem) {
                existingItem.quantity += newItem.quantity;
            } else {
                pedidosExistentes.push({ ...newItem }); // Clonar el objeto para no modificar el carrito directamente
            }
        });

        // Guardar el pedido combinado y actualizado
        localStorage.setItem(clavePedidoMesa, JSON.stringify(pedidosExistentes));

        alert(`Productos añadidos a la Mesa ${mesaNumeroActivo}.`);

        // Vaciar el carrito de la interfaz y del localStorage
        cart = [];
        updateCartDisplay();
        closeCart();
        localStorage.removeItem('cart');

        // Opcional: ofrecer navegar de vuelta a la página de mesas
        if (confirm('¿Desea volver a la página de mesas?')) {
            window.location.href = `/mesas/?mesa_id=${mesaIdActiva}&mesa_numero=${mesaNumeroActivo}`;
        }
    });

    // Vaciar carrito
    emptyCartButton.addEventListener('click', function() {
        if (confirm('¿Está seguro que desea vaciar el carrito?')) {
            cart = [];
            updateCartDisplay();
        }
    });

    // === Actualizar la visualización del carrito ===
    function updateCartDisplay() {
        cartItems.innerHTML = ''; // Limpiar visualización actual

        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        cartCount.textContent = totalItems;

        if (cart.length === 0) {
            cartItems.innerHTML = '<div class="empty-cart-message" style="text-align: center; padding: 20px; color: #aaa;">Su carrito está vacío</div>';
            cartTotalAmount.textContent = '$0';
            return;
        }

        cart.forEach(item => {
            const cartItemElement = document.createElement('div');
            cartItemElement.className = 'cart-item';
            cartItemElement.innerHTML = `
                <div class="cart-item-image">
                    <img src="${item.imgSrc}" alt="${item.title}">
                </div>
                <div class="cart-item-details">
                    <div class="cart-item-title">${item.title}</div>
                    <div class="cart-item-option">${item.option}</div>
                    <div class="cart-item-price">$${item.price.toFixed(2)}</div>

                    <div class="cart-item-controls">
                        <div class="cart-item-quantity-control">
                            <button class="quantity-btn decrease-quantity" data-id="${item.id}" data-option="${item.option}">-</button>
                            <span class="cart-quantity">${item.quantity}</span>
                            <button class="quantity-btn increase-quantity" data-id="${item.id}" data-option="${item.option}">+</button>
                        </div>
                        <button class="remove-item" data-id="${item.id}" data-option="${item.option}">Eliminar</button>
                    </div>
                </div>
            `;
            cartItems.appendChild(cartItemElement);
        });

        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cartTotalAmount.textContent = `$${total.toFixed(2)}`;

        updateCartStorage(); // Guardamos el carrito en localStorage

        // Delegación de eventos para botones de cantidad y eliminar (mejora de rendimiento)
        cartItems.querySelectorAll('.increase-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const option = this.getAttribute('data-option');
                const item = cart.find(i => i.id == id && i.option === option);
                if (item) {
                    item.quantity += 1;
                    updateCartDisplay();
                }
            });
        });

        cartItems.querySelectorAll('.decrease-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const option = this.getAttribute('data-option');
                const itemIndex = cart.findIndex(i => i.id == id && i.option === option);
                if (itemIndex !== -1) {
                    if (cart[itemIndex].quantity > 1) {
                        cart[itemIndex].quantity -= 1;
                    } else {
                        cart.splice(itemIndex, 1);
                    }
                    updateCartDisplay();
                }
            });
        });

        cartItems.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const option = this.getAttribute('data-option');
                const itemIndex = cart.findIndex(i => i.id == id && i.option === option);
                if (itemIndex !== -1) {
                    cart.splice(itemIndex, 1);
                    updateCartDisplay();
                }
            });
        });
    }

    // === Funcionalidad del Menú Hamburguesa (separada para mejor legibilidad) ===
    const menuToggle = document.getElementById('menuToggle');
    const mainMenu = document.getElementById('mainMenu'); // Asumiendo que este es el ID de tu menú principal
    const hamburgerBtn = document.querySelector('.hamburger-btn'); // Si tienes un botón específico para el menú principal

    if (menuToggle && mainMenu) {
        menuToggle.addEventListener('click', function() {
            mainMenu.classList.toggle('active');
            if (hamburgerBtn) {
                hamburgerBtn.classList.toggle('active'); // Para el ícono de hamburguesa
            }
        });

        document.querySelectorAll('.link').forEach(link => { // Asumiendo que los enlaces del menú tienen clase 'link'
            link.addEventListener('click', function() {
                if (window.innerWidth <= 600) { // Cierra solo en móviles
                    mainMenu.classList.remove('active');
                    if (hamburgerBtn) {
                        hamburgerBtn.classList.remove('active');
                    }
                }
            });
        });

        document.addEventListener('click', function(event) {
            const isClickInsideMenu = mainMenu.contains(event.target);
            const isClickOnToggle = menuToggle.contains(event.target);
            const isClickOnHamburgerBtn = hamburgerBtn && hamburgerBtn.contains(event.target);

            if (!isClickInsideMenu && !isClickOnToggle && !isClickOnHamburgerBtn && mainMenu.classList.contains('active')) {
                mainMenu.classList.remove('active');
                if (hamburgerBtn) {
                    hamburgerBtn.classList.remove('active');
                }
            }
        });
    }

    // === Scroll del Menú Desplegable en Escritorio ===
    const menuContainer = document.querySelector(".menu-container");
    const mainContentArea = document.querySelector("main"); // Asegúrate de que 'main' sea el contenedor con scroll

    if (menuContainer && mainContentArea) {
        let lastScrollTop = 0;

        function handleScroll() {
            if (window.innerWidth <= 767) {
                menuContainer.classList.remove("menu-fixed", "menu-hidden");
                return;
            }

            let currentScrollTop = mainContentArea.scrollTop || document.documentElement.scrollTop;

            if (currentScrollTop > 350) {
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

        // Agrega el evento de scroll al contenedor principal si es que tiene scroll
        mainContentArea.addEventListener("scroll", handleScroll);
        // Si el scroll principal está en el window/document, usa eso
        window.addEventListener("scroll", handleScroll);
    }


    // === Inicializar visualización del carrito al cargar la página ===
    updateCartDisplay();
});