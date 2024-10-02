// Получаем ссылки на элементы
const homeSection = document.getElementById('home');
const catalogSection = document.getElementById('catalog');
const cartSection = document.getElementById('cart');
const registerSection = document.getElementById('register');
const registerBtn = document.getElementById('register-btn');
const userName = document.getElementById('user-name');
const userInfo = document.getElementById('user-info');
const cartCount = document.getElementById('cart-count');
const productsContainer = document.getElementById('products-container');
const cartItemsContainer = document.getElementById('cart-items');
const orderMessage = document.getElementById('order-message');
const registrationMessage = document.getElementById('registration-message');

// Скрытие всех страниц
function hideAllPages() {
    homeSection.style.display = 'none';
    catalogSection.style.display = 'none';
    cartSection.style.display = 'none';
    registerSection.style.display = 'none';
}

// Показать главную страницу
document.getElementById('home-btn').addEventListener('click', () => {
    hideAllPages();
    homeSection.style.display = 'block';
});

// Показать каталог
document.getElementById('catalog-btn').addEventListener('click', () => {
    hideAllPages();
    catalogSection.style.display = 'block';
    loadProducts('toys'); // Загружаем игрушки по умолчанию
});

// Показать корзину
document.getElementById('cart-btn').addEventListener('click', () => {
    hideAllPages();
    cartSection.style.display = 'block';
});

// Показать форму регистрации
registerBtn.addEventListener('click', () => {
    hideAllPages();
    registerSection.style.display = 'block';
    registrationMessage.style.display = 'none'; // Скрываем сообщение регистрации
});

// Обработка регистрации
document.getElementById('register-form').addEventListener('submit', (event) => {
    event.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    // Успешная регистрация
    userName.textContent = username;
    userName.style.display = 'inline';
    userInfo.style.display = 'inline';
    registerBtn.style.display = 'none';
    
    // Скрываем форму регистрации и показываем главную страницу
    hideAllPages();
    homeSection.style.display = 'block'; 
    registrationMessage.style.display = 'none'; // Скрываем сообщение регистрации
});

// Загрузка продуктов в зависимости от категории
document.querySelectorAll('.category').forEach(category => {
    category.addEventListener('click', (event) => {
        const selectedCategory = event.target.dataset.category;
        loadProducts(selectedCategory);
    });
});

// Данные товаров по категориям
const productsByCategory = {
    toys: [
        { id: 1, name: "Мяч", price: 500 },
        { id: 2, name: "Кукла", price: 700 }
    ],
    clothes: [
        { id: 3, name: "Футболка", price: 1000 },
        { id: 4, name: "Джинсы", price: 1500 }
    ],
    food: [
        { id: 5, name: "Хлеб", price: 200 },
        { id: 6, name: "Молоко", price: 150 }
    ]
};

// Загрузка товаров в контейнер
function loadProducts(category) {
    productsContainer.innerHTML = ''; // Очищаем контейнер
    const products = productsByCategory[category];

    products.forEach(product => {
        const productElement = document.createElement('div');
        productElement.classList.add('product');
        productElement.innerHTML = `
            <h3>${product.name}</h3>
            <p>Цена: ${product.price} руб.</p>
            <label for="quantity-${product.id}">Количество:</label>
            <input type="number" id="quantity-${product.id}" min="1" value="1">
            <button class="add-to-cart" data-id="${product.id}" data-name="${product.name}" data-price="${product.price}">Добавить в корзину</button>
        `;
        productsContainer.appendChild(productElement);
    });

    // Обработка добавления товаров в корзину
    document.querySelectorAll('.add-to-cart').forEach(button => {
        button.addEventListener('click', (event) => {
const productId = event.target.dataset.id;
            const productName = event.target.dataset.name;
            const productPrice = event.target.dataset.price;
            const productQuantity = document.getElementById('quantity-' + productId).value;

            addToCart(productId, productName, productPrice, productQuantity);
        });
    });
}

// Корзина
let cart = [];

// Добавление товаров в корзину
function addToCart(id, name, price, quantity) {
    const existingProduct = cart.find(product => product.id === id);
    if (existingProduct) {
        existingProduct.quantity += parseInt(quantity);
    } else {
        cart.push({ id, name, price, quantity: parseInt(quantity) });
    }
    updateCart();
}

// Обновление корзины
function updateCart() {
    cartCount.textContent = cart.reduce((sum, product) => sum + product.quantity, 0);
    cartItemsContainer.innerHTML = '';

    cart.forEach(product => {
        const cartItem = document.createElement('div');
        cartItem.classList.add('cart-item');
        cartItem.innerHTML = `
            <p>${product.name} - ${product.quantity} шт. по ${product.price} руб.</p>
            <button class="remove-item" data-id="${product.id}">Удалить</button>
        `;
        cartItemsContainer.appendChild(cartItem);
    });

    // Обработка удаления товаров из корзины
    document.querySelectorAll('.remove-item').forEach(button => {
        button.addEventListener('click', (event) => {
            const productId = event.target.dataset.id;
            cart = cart.filter(product => product.id !== productId);
            updateCart();
        });
    });
}

// Обработка оформления заказа
document.getElementById('checkout').addEventListener('click', () => {
    if (cart.length > 0) {
        orderMessage.textContent = 'Заказ оформлен! Спасибо за покупку.';
        orderMessage.style.display = 'block';
        cart = []; // Очистка корзины после оформления заказа
        updateCart(); // Обновляем корзину
    } else {
        orderMessage.textContent = 'Ваша корзина пуста!';
        orderMessage.style.display = 'block';
    }
});

// Начальная загрузка
hideAllPages();
homeSection.style.display = 'block'; 