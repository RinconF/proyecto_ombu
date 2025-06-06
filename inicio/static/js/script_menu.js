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
    let mesaIdActiva = getUrlParameter('mesa_id') || localStorage.getItem('mesaActivaId');
    let mesaNumeroActivo = getUrlParameter('mesa_numero') || localStorage.getItem('mesaActivaNumero');

    // Referencias a elementos del DOM
    const modalPrice = document.createElement('div');
    const cards = document.querySelectorAll(".card");
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const modalImage = document.getElementById("modal-image");
    const modalSelect = document.getElementById("modal-select");
    const closeModal = document.querySelector(".close");
    // === CAMBIO: Nueva referencia al elemento de cantidad disponible en el modal ===
    const modalAvailableQuantity = document.getElementById("modal-available-quantity");


    let modalAddToCartBtn = document.getElementById("modal-add-to-cart");
    if (!modalAddToCartBtn) {
        modalAddToCartBtn = document.createElement('button');
        modalAddToCartBtn.id = 'modal-add-to-cart';
        modalAddToCartBtn.textContent = 'Agregar al carrito';
        modalAddToCartBtn.style.marginTop = '15px';
        modalAddToCartBtn.style.width = '100%';
        modalAddToCartBtn.classList.add('button'); // Asegúrate que esta clase exista o cámbiala
    }

    const modalInfo = modal.querySelector('.modal-info');
    if (modalInfo && modalTitle) {
        modalInfo.insertBefore(modalPrice, modalTitle.nextSibling);
        if (!document.getElementById("modal-add-to-cart")) {
            modalInfo.appendChild(modalAddToCartBtn);
        }
    }



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

    function updateModalAvailableQuantity() {
        console.log("updateModalAvailableQuantity called"); // DEBUG: Para confirmar que se llama
        if (currentProductData.card && modalAvailableQuantity) {
            // Obtener la cantidad disponible actual desde el dataset de la tarjeta
            const quantity = parseInt(currentProductData.card.dataset.cantidadDisponibleActual);
            console.log("Modal Product ID:", currentProductData.card.dataset.id); // DEBUG
            console.log("Modal Current available quantity:", quantity); // DEBUG

            let textToDisplay;
            if (quantity > 0) {
                textToDisplay = `Cantidad disponible: ${quantity}`;
                modalAddToCartBtn.disabled = false;
            } else {
                textToDisplay = `No hay unidades disponibles.`;
                modalAddToCartBtn.disabled = true;
            }
            modalAvailableQuantity.textContent = textToDisplay;
            console.log("Text applied to modal-available-quantity:", textToDisplay); // DEBUG
        } else {
            console.log("updateModalAvailableQuantity: currentProductData.card or modalAvailableQuantity is null/undefined.");
            if (!currentProductData.card) console.log("currentProductData.card is null/undefined.");
            if (!modalAvailableQuantity) console.log("modalAvailableQuantity is null/undefined.");
        }
    }


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
        // cartIcon.style.display = 'block'; // ELIMINADA EN REVISIÓN ANTERIOR
        cartOpen = false;
    }

    // === Inicialización de Navegación ===
    const menuLinks = document.querySelectorAll('.main-nav a');
    menuLinks.forEach(link => {
        const originalHref = link.getAttribute('href');
        if (originalHref && !originalHref.startsWith('#') && !originalHref.includes('?')) {
            if (mesaIdActiva && mesaNumeroActivo) {
                link.href = `${originalHref}?mesa_id=${mesaIdActiva}&mesa_numero=${mesaNumeroActivo}`;
            }
        }
    });

    // === Gestión del Modal de Productos ===
    modalPrice.className = 'modal-price';
    modalPrice.style.fontWeight = 'bold';
    modalPrice.style.fontSize = '1.2rem';
    modalPrice.style.margin = '10px 0';
    modalPrice.style.color = '#20AB47';


    // --- NUEVA FUNCIÓN: Actualizar el estado del botón de la tarjeta ---
    function updateCardButtonState(card) {
        const addButton = card.querySelector('.add-to-cart-btn'); // Asume que este es tu botón principal de acción
        const productId = card.dataset.id;
        const initialAvailableQuantity = parseInt(card.dataset.cantidadDisponible);
        const itemInCart = cart.find(item => item.id == productId && item.option === 'Regular'); // Buscar el ítem 'Regular' en el carrito
        const quantityInCart = itemInCart ? itemInCart.quantity : 0;

        // === CAMBIO: Calcular la cantidad disponible para mostrar ===
        const remainingQuantity = initialAvailableQuantity - quantityInCart;
        card.dataset.cantidadDisponibleActual = remainingQuantity; // Guardar la cantidad actual en el dataset de la tarjeta
        console.log(`Card ${productId} updated: initial=${initialAvailableQuantity}, inCart=${quantityInCart}, remaining=${remainingQuantity}`);

        if (!addButton) return; // Salir si el botón no existe (ej. es el botón "Ver más")

        // Prioridad: Si no hay disponibilidad inicial, o si la cantidad en carrito es >= a la disponible
        if (remainingQuantity <= 0) { // Usamos remainingQuantity
            addButton.innerHTML = 'No disponible'; // O "Agotado" si prefieres
            addButton.disabled = true;
            addButton.classList.add('product-disabled-btn');
            addButton.classList.remove('product-action-btn');
        } else {
            addButton.innerHTML = '<span class="button-text">+</span>';
            addButton.disabled = false;
            addButton.classList.remove('product-disabled-btn');
            addButton.classList.add('product-action-btn');
        }
    }

    // --- NUEVA FUNCIÓN: Actualizar la cantidad disponible en el modal ---
    document.addEventListener('click', function(e) {
        if (e.target.closest('.add-to-cart-btn') && !e.target.closest('.add-to-cart-btn').disabled) {
            const button = e.target.closest('.add-to-cart-btn');
            const card = button.closest('.card');

            if (card.id === 'modal-card') return; // Evitar el botón del modal si lo tienes

            e.stopPropagation();

            const productId = card.dataset.id;
            const imgSrc = card.querySelector('img').src;
            const title = card.querySelector('.main-card > span').textContent;
            const priceElement = card.querySelector('.footer-card > span');
            const price = parseFloat(priceElement.textContent.replace(/[^0-9.-]+/g, '')) || 0;
            const initialAvailableQuantity = parseInt(card.dataset.cantidadDisponible);

            // Importante: Considerar si el producto ya está en el carrito, y si lo está con qué opción
            const existingItemIndex = cart.findIndex(item => item.id == productId && item.option === 'Regular'); // Asume 'Regular' si no hay opciones
            const currentQuantityInCart = existingItemIndex !== -1 ? cart[existingItemIndex].quantity : 0;

            if (currentQuantityInCart >= initialAvailableQuantity) {
                alert('No hay más unidades disponibles de este producto.');
                updateCardButtonState(card); // Asegurar que el botón se actualice
                return;
            }

            if (existingItemIndex !== -1) {
                cart[existingItemIndex].quantity += 1;
            } else {
                const cartItem = {
                    id: productId,
                    imgSrc,
                    title,
                    price,
                    priceDisplay: priceElement.textContent,
                    quantity: 1,
                    option: 'Regular' // Opción por defecto
                };
                cart.push(cartItem);
            }
            updateCartDisplay();

            // Si el modal está abierto para este producto, actualiza su cantidad disponible
            if (modal.style.display === "flex" && currentProductData.card && currentProductData.card.dataset.id == productId) {
                console.log("Updating modal quantity after '+' button click"); // DEBUG
                updateModalAvailableQuantity();
            }
        }
    });

    // Funcionalidad del modal al hacer clic en la tarjeta
    cards.forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.classList.contains('ver-mas-btn') || e.target.closest('.add-to-cart-btn')) {
                return;
            }

            const title = card.getAttribute('data-title') || card.querySelector('.main-card > span').textContent;
            const imgSrc = card.getAttribute('data-image') || card.querySelector('img').src;
            const description = card.querySelector('.truncated-text').textContent;
            const priceElement = card.querySelector('.footer-card > span');
            const basePrice = priceElement ? priceElement.textContent : '$0';
            const basePriceValue = parseFloat(basePrice.replace(/[^0-9.-]+/g, '')) || 0;

            const modalDescription = document.getElementById('modal-description');
            if (modalDescription) {
                modalDescription.textContent = description;
            }

            currentProductData.card = card; // Guarda la referencia a la tarjeta actual
            currentProductData.basePrice = basePriceValue;
            currentProductData.currentPrice = basePriceValue;
            currentProductData.currentPriceDisplay = basePrice;

            currentProductData.options = {
                'Regular': {
                    price: basePriceValue,
                    priceDisplay: basePrice
                }
            };

            modalTitle.textContent = title;
            modalImage.src = imgSrc;
            modalImage.alt = title;
            modalPrice.textContent = basePrice;

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

                        currentProductData.options[option] = {
                            price: basePriceValue,
                            priceDisplay: basePrice
                        };
                    });
                } else {
                    const optionElement = document.createElement('option');
                    optionElement.value = "Regular";
                    optionElement.textContent = "Regular";
                    modalSelect.appendChild(optionElement);
                }
            } catch (e) {
                console.error("Error al analizar opciones:", e);
                const optionElement = document.createElement('option');
                optionElement.value = "Regular";
                optionElement.textContent = "Regular";
                modalSelect.appendChild(optionElement);
            }

            modal.style.display = "flex";
            console.log("Modal opened, calling updateModalAvailableQuantity()"); 
            // === CAMBIO: Actualizar la cantidad disponible del modal al abrirlo ===
            updateModalAvailableQuantity();
        });
    });

    // Evento de cambio de opción en el modal
    modalSelect.addEventListener('change', function() {
        const selectedOption = this.value;
        if (currentProductData.options && currentProductData.options[selectedOption]) {
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
        // cartIcon.style.display = 'none'; // ELIMINADA EN REVISIÓN ANTERIOR
        cartOpen = true;
    });

    closeCartBtn.addEventListener('click', closeCart);
    overlay.addEventListener('click', closeCart);

    // Agregar al carrito desde el modal (botón "Agregar al carrito")
    modalAddToCartBtn.addEventListener('click', function() {
        const title = modalTitle.textContent;
        const imgSrc = modalImage.src;
        const productId = currentProductData.card.dataset.id;
        const initialAvailableQuantity = parseInt(currentProductData.card.dataset.cantidadDisponible); // Cantidad inicial del producto

        let option = 'Regular';
        if (modalSelect && modalSelect.value) {
            option = modalSelect.value;
        }

        const price = currentProductData.currentPrice;
        const priceDisplay = currentProductData.currentPriceDisplay;

        // Comprobación de disponibilidad antes de añadir
        const existingItemIndex = cart.findIndex(item => item.id == productId && item.option === option);
        const currentQuantityInCart = existingItemIndex !== -1 ? cart[existingItemIndex].quantity : 0;

        if (currentQuantityInCart >= initialAvailableQuantity) {
            alert('No hay más unidades disponibles de este producto.');
            // Ya que el modal se cierra, la actualización de la tarjeta es la que importa.
            // updateModalAvailableQuantity(); // Podrías querer esto si NO cierras el modal
            return;
        }

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
        modal.style.display = 'none'; // El modal se cierra aquí

        // Animación del contador (si aún la quieres)
        cartCount.style.transform = 'scale(1.3)';
        setTimeout(() => {
            cartCount.style.transform = 'scale(1)';
            cartContainer.classList.add('open');
            overlay.style.display = 'block';
            cartOpen = true;
        }, 300);

        // Ya que el modal se cierra, la próxima vez que se abra, la cantidad disponible
        // se actualizará por la llamada en el evento click de la tarjeta.
        // Si el modal NO se cerrara, entonces sí llamarías a updateModalAvailableQuantity() aquí.
    });

    // === Finalizar compra ===
    checkoutButton.addEventListener('click', function() {
        if (cart.length === 0) {
            alert('Su carrito está vacío');
            return;
        }

        if (!mesaIdActiva || !mesaNumeroActivo) {
            alert('No se pudo identificar la mesa activa. Por favor, asegúrese de haber seleccionado una mesa.');
            return;
        }

        const clavePedidoMesa = `pedido_mesa_${mesaIdActiva}`;
        const pedidosExistentes = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];

        cart.forEach(newItem => {
            const existingItem = pedidosExistentes.find(
                p => p.id == newItem.id && p.option === newItem.option
            );
            if (existingItem) {
                existingItem.quantity += newItem.quantity;
            } else {
                pedidosExistentes.push({ ...newItem });
            }
        });

        localStorage.setItem(clavePedidoMesa, JSON.stringify(pedidosExistentes));

        alert(`Productos añadidos a la Mesa ${mesaNumeroActivo}.`);

        cart = [];
        updateCartDisplay(); // Esto ahora también actualizará el estado de los botones de las tarjetas y la cantidad disponible en el modal (si estuviera abierto)
        closeCart();
        localStorage.removeItem('cart');

        if (confirm('¿Desea volver a la página de mesas?')) {
            window.location.href = `/mesas/?mesa_id=${mesaIdActiva}&mesa_numero=${mesaNumeroActivo}`;
        }
    });

    // Vaciar carrito
    emptyCartButton.addEventListener('click', function() {
        if (confirm('¿Está seguro que desea vaciar el carrito?')) {
            cart = [];
            updateCartDisplay(); // Esto ahora también actualizará el estado de los botones de las tarjetas y la cantidad disponible en el modal (si estuviera abierto)
        }
    });

    // === Actualizar la visualización del carrito ===
    function updateCartDisplay() {
        cartItems.innerHTML = '';

        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        cartCount.textContent = totalItems;

        if (totalItems === 0) {
            cartCount.classList.add('cart-icon-hidden');
        } else {
            cartCount.classList.remove('cart-icon-hidden');
        }

        if (cart.length === 0) {
            cartItems.innerHTML = '<div class="empty-cart-message" style="text-align: center; padding: 20px; color: #aaa;">Su carrito está vacío</div>';
            cartTotalAmount.textContent = '$0';
            cards.forEach(card => updateCardButtonState(card)); // Asegurarse de actualizar todas las tarjetas
            // === CAMBIO: Actualizar la cantidad disponible en el modal si está abierto y el producto actual es afectado ===
            if (modal.style.display === "flex" && currentProductData.card) {
                updateModalAvailableQuantity();
            }
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

        updateCartStorage();

        // === IMPORTANTE: Actualizar el estado de los botones de las tarjetas después de cualquier cambio en el carrito ===
        cards.forEach(card => {
            updateCardButtonState(card);
        });

        // === CAMBIO: Actualizar la cantidad disponible en el modal si está abierto y el producto actual es afectado ===
        if (modal.style.display === "flex" && currentProductData.card) {
            console.log("Updating modal quantity from updateCartDisplay()");
            updateModalAvailableQuantity();
        }


        // Delegación de eventos para botones de cantidad y eliminar (mejora de rendimiento)
        cartItems.querySelectorAll('.increase-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const option = this.getAttribute('data-option');
                const item = cart.find(i => i.id == id && i.option === option);
                if (item) {
                    const card = document.querySelector(`.card[data-id="${id}"]`);
                    const initialAvailableQuantity = parseInt(card.dataset.cantidadDisponible); // Usa la cantidad inicial
                    if (item.quantity < initialAvailableQuantity) { // Verificar disponibilidad contra la cantidad inicial
                        item.quantity += 1;
                    } else {
                        alert('No hay más unidades disponibles de este producto.');
                    }
                    updateCartDisplay();
                    // === CAMBIO: Actualizar la cantidad disponible en el modal si está abierto y el producto actual es afectado ===
                    if (modal.style.display === "flex" && currentProductData.card && currentProductData.card.dataset.id == id) {
                        console.log("Updating modal quantity after decrease-quantity");
                        updateModalAvailableQuantity();
                    }
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
                    // === CAMBIO: Actualizar la cantidad disponible en el modal si está abierto y el producto actual es afectado ===
                    if (modal.style.display === "flex" && currentProductData.card && currentProductData.card.dataset.id == id) {
                        updateModalAvailableQuantity();
                    }
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
                    // === CAMBIO: Actualizar la cantidad disponible en el modal si está abierto y el producto actual es afectado ===
                    if (modal.style.display === "flex" && currentProductData.card && currentProductData.card.dataset.id == id) {
                        console.log("Updating modal quantity after remove-item");
                        updateModalAvailableQuantity();
                    }
                }
            });
        });
    }

    // === Funcionalidad del Menú Hamburguesa ===
    const menuToggle = document.getElementById('menuToggle');
    const mainMenu = document.getElementById('mainMenu');
    const hamburgerBtn = document.querySelector('.hamburger-btn');

    if (menuToggle && mainMenu) {
        menuToggle.addEventListener('click', function() {
            mainMenu.classList.toggle('active');
            if (hamburgerBtn) {
                hamburgerBtn.classList.toggle('active');
            }
        });

        document.querySelectorAll('.link').forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 600) {
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
    const mainContentArea = document.querySelector("main");

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
                menuContainer.classList.add("menu-hidden");
            } else {
                menuContainer.classList.remove("menu-hidden");
            }

            lastScrollTop = currentScrollTop;
        }

        mainContentArea.addEventListener("scroll", handleScroll);
        window.addEventListener("scroll", handleScroll);
    }

    // === Inicializar visualización del carrito y el estado de los botones de las tarjetas al cargar la página ===
    updateCartDisplay();
});