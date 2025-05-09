document.addEventListener("DOMContentLoaded", () => {
    // Variables globales
    inicializarNavegacionConMesa();
    let cart = JSON.parse(localStorage.getItem('cart')) || []; // Recuperar carrito desde localStorage
    let cartOpen = false;
    let currentProductData = {
        card: null,
        options: {},
        currentPrice: 0,
        currentPriceDisplay: '',
        basePrice: 0
    };

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

    // Función para obtener un parámetro de la URL
    function getUrlParameter(name) {
        name = name.replace(/[\[]/, '\\[').replace(/[\]]/, '\\]');
        const regex = new RegExp('[\\?&]' + name + '=([^&#]*)');
        const results = regex.exec(location.search);
        return results === null ? '' : decodeURIComponent(results[1].replace(/\+/g, ' '));
    }

    // Obtener el mesaId de la URL
    const mesaIdDesdeUrl = getUrlParameter('mesa'); // Se obtiene el mesaId de la URL al cargar la página
    const idmesa = document.getElementById('checkout-button')
    idmesa.textContent = "Finalizar compra en mesa "+ mesaIdDesdeUrl;


    // Función para agregar a todas las páginas - poner en un archivo común
    function inicializarNavegacionConMesa() {
        // Obtener el ID de mesa de la URL
        const urlParams = new URLSearchParams(window.location.search);
        const mesaId = urlParams.get('mesa');

        if (mesaId) {
            // Guardar en localStorage como referencia de respaldo
            localStorage.setItem('mesaActivaId', mesaId);

            // Actualizar todos los enlaces de navegación para incluir el ID de mesa
            document.querySelectorAll('a').forEach(link => {
                // No modificar enlaces externos o anclas
                if (link.href.startsWith(window.location.origin) && !link.href.includes('#')) {
                    const url = new URL(link.href);
                    url.searchParams.set('mesa', mesaId);
                    link.href = url.toString();
                }
            });

            // Si existe un elemento para mostrar la mesa activa, actualizarlo
            const mesaActivaElement = document.getElementById('mesa-activa');
            if (mesaActivaElement) {
                mesaActivaElement.textContent = `Mesa ${mesaId}`;
            }

            // Actualizar botón de finalizar compra si existe
            const checkoutButton = document.getElementById('checkout-button');
            if (checkoutButton) {
                checkoutButton.textContent = `Finalizar compra en mesa ${mesaId}`;
            }
        } else {
            // Si no hay mesa en URL pero sí en localStorage, redirigir con el parámetro
            const mesaGuardada = localStorage.getItem('mesaActivaId');
            if (mesaGuardada && !window.location.pathname.includes('mesas.html')) {
                window.location.href = window.location.pathname + `?mesa=${mesaGuardada}`;
                return;
            }
        }
    }

    // Función para regresar a la página de mesas manteniendo información
    function volverAMesas() {
        const mesaId = localStorage.getItem('mesaActivaId');
        window.location.href = '/pages/mesas.html?ultima_mesa=' + mesaId;
    }

    // Función para navegar a una categoría manteniendo la mesa
    function navegarACategoria(categoria) {
        const mesaId = localStorage.getItem('mesaActivaId');
        if (!mesaId) {
            alert('Por favor seleccione una mesa primero');
            return;
        }
        window.location.href = `/pages/menu_mesero/${categoria}.html?mesa=${mesaId}`;
    }


    // Función para actualizar el carrito en localStorage
    function updateCartStorage() {
        localStorage.setItem('cart', JSON.stringify(cart));
    }




    
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
    }

    // Añadir el elemento de precio al modal después del título
    const modalInfo = modal.querySelector('.modal-info');
    if (modalInfo) {
        if (modalTitle) {
            modalInfo.insertBefore(modalPrice, modalTitle.nextSibling);
        }

        // Asegurarse de que el botón de agregar al carrito esté al final
        if (!document.getElementById("modal-add-to-cart")) {
            modalInfo.appendChild(modalAddToCartBtn);
        }
    }

    // Añadir botones "Agregar al carrito" a todas las tarjetas
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

    // Funcionalidad del modal
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
            const basePriceValue = parseInt(basePrice.replace(/\D/g, '')) || 0;

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
                // Verificar si hay opciones para este producto
                const options = card.getAttribute('data-options');
                if (options) {
                    const optionsArray = JSON.parse(options);
                    optionsArray.forEach(option => {
                        const optionElement = document.createElement('option');
                        optionElement.value = option;
                        optionElement.textContent = option;
                        modalSelect.appendChild(optionElement);

                        // Establecer el mismo precio para todas las opciones (puedes modificar esto si las opciones tienen diferentes precios)
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

    // Carrito de compras - Abrir y cerrar
    cartIcon.addEventListener('click', function() {
        cartContainer.classList.add('open');
        overlay.style.display = 'block';
        cartOpen = true;
    });

    closeCartBtn.addEventListener('click', closeCart);
    overlay.addEventListener('click', closeCart);

    function closeCart() {
        cartContainer.classList.remove('open');
        overlay.style.display = 'none';
        cartOpen = false;
    }

    // Agregar al carrito desde las tarjetas
    document.querySelectorAll('.add-to-cart-btn').forEach((button, index) => {
        button.addEventListener('click', function(e) {
            e.stopPropagation(); // Evitar que se abra el modal

            const card = this.closest('.card');
            const imgSrc = card.querySelector('img').src;
            const title = card.querySelector('.main-card > span').textContent;
            const priceElement = card.querySelector('.footer-card > span');
            const price = priceElement ? priceElement.textContent : '$0';
            const priceValue = parseInt(price.replace(/\D/g, '')) || 0;

            // Verificar si el artículo ya está en el carrito
            const existingItemIndex = cart.findIndex(item => item.title === title && item.option === 'Regular');

            if (existingItemIndex !== -1) {
                // Artículo ya en el carrito, aumentar cantidad
                cart[existingItemIndex].quantity += 1;
                updateCartDisplay();
            } else {
                // Nuevo artículo, agregar al carrito
                const cartItem = {
                    id: Date.now() + index,
                    imgSrc,
                    title,
                    price: priceValue,
                    priceDisplay: price,
                    quantity: 1,
                    option: 'Regular' // Opción predeterminada
                };

                cart.push(cartItem);
                updateCartDisplay();
            }

            // Animación para el icono del carrito
            cartCount.style.transform = 'scale(1.3)';
            setTimeout(() => {
                cartCount.style.transform = 'scale(1)';
            }, 300);
        });
    });

    // Agregar al carrito desde el modal
    modalAddToCartBtn.addEventListener('click', function() {
        const title = modalTitle.textContent;
        const imgSrc = modalImage.src;

        // Obtener opción seleccionada del modal
        let option = 'Regular';
        if (modalSelect && modalSelect.value) {
            option = modalSelect.value;
        }

        // Usar el precio actual del producto
        const price = currentProductData.currentPrice;
        const priceDisplay = currentProductData.currentPriceDisplay;

        if (price > 0) {
            // Verificar si el artículo con el mismo título y opción está en el carrito
            const existingItemIndex = cart.findIndex(item =>
                item.title === title && item.option === option
            );

            if (existingItemIndex !== -1) {
                cart[existingItemIndex].quantity += 1;
            } else {
                const cartItem = {
                    id: Date.now(),
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

    // Finalizar compra (MODIFICADO PARA GUARDAR CON mesaId)
    checkoutButton.addEventListener('click', function() {
        if (cart.length === 0) {
            alert('Su carrito está vacío');
            return;
        }

        const mesaId = localStorage.getItem('mesaActivaId') || getUrlParameter('mesa');

        if (mesaId) {
            const clavePedidoMesa = `pedido_mesa_${mesaId}`;
            
            // Obtener pedidos existentes para esta mesa
            const pedidosExistentes = JSON.parse(localStorage.getItem(clavePedidoMesa)) || [];
            
            // Combinar con los nuevos productos
            const pedidoActualizado = [...pedidosExistentes, ...cart];
            
            // Guardar el pedido combinado
            localStorage.setItem(clavePedidoMesa, JSON.stringify(pedidoActualizado));
            
            alert(`Productos añadidos a la Mesa ${mesaId}. Total actual: ${cartTotalAmount.textContent}`);
            cart = []; // vaciar el carrito
            updateCartDisplay();
            closeCart();
            
            localStorage.removeItem('cart'); // limpiar carrito temporal
            
            // Opcional: ofrecer navegar de vuelta a la página de mesas
            if (confirm('¿Desea volver a la página de mesas?')) {
                volverAMesas();
            }
        } else {
            alert('No se pudo identificar el ID de la mesa para guardar el pedido.');
        }

    });

    // Vaciar carrito
    emptyCartButton.addEventListener('click', function() {
        if (confirm('¿Está seguro que desea vaciar el carrito?')) {
            cart = [];
            updateCartDisplay();
        }
    });

    // Actualizar la visualización del carrito
    function updateCartDisplay() {
        // Limpiar visualización actual
        cartItems.innerHTML = '';

        // Actualizar contador de artículos
        const totalItems = cart.reduce((total, item) => total + item.quantity, 0);
        cartCount.textContent = totalItems;

        if (cart.length === 0) {
            cartItems.innerHTML = '<div class="empty-cart-message" style="text-align: center; padding: 20px; color: #aaa;">Su carrito está vacío</div>';
            cartTotalAmount.textContent = '$0';
            return;
        }

        // Agregar artículos a la visualización
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
                    <div class="cart-item-price">${item.priceDisplay}</div>

                    <div class="cart-item-controls">
                        <div class="cart-item-quantity-control">
                            <button class="quantity-btn decrease-quantity" data-id="${item.id}">-</button>
                            <span class="cart-quantity">${item.quantity}</span>
                            <button class="quantity-btn increase-quantity" data-id="${item.id}">+</button>
                        </div>
                        <button class="remove-item" data-id="${item.id}">Eliminar</button>
                    </div>
                </div>
            `;

            cartItems.appendChild(cartItemElement);
        });

        // Calcular y actualizar el total
        const total = cart.reduce((sum, item) => sum + (item.price * item.quantity), 0);
        cartTotalAmount.textContent = `$${total.toLocaleString()}`;

        // Guardamos el carrito en localStorage
        updateCartStorage();

        // Agregar eventos a los botones de cantidad
        document.querySelectorAll('.increase-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const item = cart.find(item => item.id == id);
                if (item) {
                    item.quantity += 1;
                    updateCartDisplay();
                }
            });
        });

        document.querySelectorAll('.decrease-quantity').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const itemIndex = cart.findIndex(item => item.id == id);
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

        document.querySelectorAll('.remove-item').forEach(button => {
            button.addEventListener('click', function() {
                const id = this.getAttribute('data-id');
                const itemIndex = cart.findIndex(item => item.id == id);
                if (itemIndex !== -1) {
                    cart.splice(itemIndex, 1);
                    updateCartDisplay();
                }
            });
        });
    }

    // Inicializar visualización del carrito
    updateCartDisplay();
});



document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.navbar-menu');
    
    if (hamburger && navMenu) {
      hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        navMenu.classList.toggle('active');
      });
      
      document.querySelectorAll('.navbar-link').forEach(link => {
        link.addEventListener('click', function() {
          hamburger.classList.remove('active');
          navMenu.classList.remove('active');
        });
      });
    }
  });


  


  // JavaScript para el menú hamburguesa
  document.addEventListener('DOMContentLoaded', function() {
    const menuToggle = document.getElementById('menuToggle');
    const mainMenu = document.getElementById('mainMenu');
    
    // Toggle menu cuando se hace clic en el botón hamburguesa
    menuToggle.addEventListener('click', function() {
      mainMenu.classList.toggle('active');
    });
    
    // Cerrar menú cuando se hace clic en un enlace
    const menuLinks = document.querySelectorAll('.link');
    menuLinks.forEach(link => {
      link.addEventListener('click', function() {
        if (window.innerWidth <= 600) {
          mainMenu.classList.remove('active');
        }
      });
    });
    
    // Cerrar menú si se hace clic fuera de él
    document.addEventListener('click', function(event) {
      const isClickInsideMenu = mainMenu.contains(event.target);
      const isClickOnToggle = menuToggle.contains(event.target);
      
      if (!isClickInsideMenu && !isClickOnToggle && mainMenu.classList.contains('active')) {
        mainMenu.classList.remove('active');
      }
    });
  });



    //    SCRIPT PARA EL   MENU DESPLEGABLE EN ESCRITORIO  (OARA QUE APAREZCA Y DESAPAREZCA AL SUBIR  Y BAJAR) SCROLL

  document.addEventListener("DOMContentLoaded", () => {
    const menuContainer = document.querySelector(".menu-container");
    const main = document.querySelector("main");
    let lastScrollTop = 0;

    function handleScroll() {
        // Verifica el ancho de la pantalla para aplicar solo en escritorio
        if (window.innerWidth <= 767) {
            menuContainer.classList.remove("menu-fixed", "menu-hidden");
            return;
        }

        let currentScrollTop = main.scrollTop || document.documentElement.scrollTop;

        if (currentScrollTop > 150) {
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

    // Agrega el evento de scroll al `main` en lugar de `window`
    main.addEventListener("scroll", handleScroll);
});


