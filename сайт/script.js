const homeSection = document.getElementById('home');
const catalogSection = document.getElementById('catalog');
const cartSection = document.getElementById('cart');
const registerBtn = document.getElementById('register-btn');
const userName = document.getElementById('user-name');
const cartCount = document.getElementById('cart-count');
const productsContainer = document.getElementById('products-container');
const cartItemsContainer = document.getElementById('cart-items');
const registrationMessage = document.getElementById('registration-message');
const registerModal = document.getElementById('register-modal');
const closeModal = document.getElementById('close-modal');
const orderMessage = document.getElementById('order-message');

let isUserRegistered = false;
let cart = [];

// Скрытие всех страниц
function hideAllPages() {
    homeSection.style.display = 'none';
    catalogSection.style.display = 'none';
    cartSection.style.display = 'none';
}

// Показ главной страницы
document.getElementById('home-btn').addEventListener('click', () => {
    hideAllPages();
    homeSection.style.display = 'block';
});

// Проверка регистрации для каталога
document.getElementById('catalog-btn').addEventListener('click', () => {
    if (!isUserRegistered) {
        hideAllPages();
        catalogSection.style.display = 'block';
        loadProducts('toys'); // Загружаем игрушки по умолчанию
    }
});

// Проверка регистрации для корзины
document.getElementById('cart-btn').addEventListener('click', () => {
     {
        hideAllPages();
        cartSection.style.display = 'block';
        loadCart();
    }
});

// Закрытие модального окна
closeModal.addEventListener('click', () => {
    registerModal.style.display = 'none';
});

// Показываем модальное окно при нажатии на кнопку "Регистрация"
document.getElementById('register-btn').addEventListener('click', () => {
    const registerModal = document.getElementById('register-modal');
    registerModal.style.display = 'flex'; // Показываем модальное окно
});

// Показываем модальное окно при нажатии на кнопку "Регистрация"
document.getElementById('register-btn').addEventListener('click', () => {
    if (!isUserRegistered) {
        // Если пользователь не зарегистрирован, показываем модальное окно
        const registerModal = document.getElementById('register-modal');
        registerModal.style.display = 'flex'; // Показываем модальное окно
    } else {
        // Если пользователь уже зарегистрирован, выводим сообщение
        alert('Вы уже зарегистрированы как ' + userName.textContent);
    }
});

// Показываем модальное окно при нажатии на кнопку "Регистрация"
registerBtn.addEventListener('click', () => {
    if (!isUserRegistered) {
        registerModal.style.display = 'flex'; // Показываем модальное окно
    } else {
        alert('Вы уже зарегистрированы как ' + userName.textContent);
    }
});

// Обработка закрытия модального окна
closeModal.addEventListener('click', () => {
    registerModal.style.display = 'none';
});

// Обработка регистрации
document.getElementById('register-form').addEventListener('submit', (event) => {
    event.preventDefault(); // Отключаем стандартное поведение формы (перезагрузку страницы)
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username && password) {
        // Скрываем модальное окно регистрации
        registerModal.style.display = 'none';

        // Сбрасываем поля ввода после регистрации
        document.getElementById('username').value = '';
        document.getElementById('password').value = '';
        registrationMessage.style.display = 'none';
        
        // После регистрации убираем возможность открыть модальное окно
        registerBtn.textContent = username; // Изменяем текст кнопки
    } else {
        // Если поля не заполнены, показываем сообщение об ошибке
        registrationMessage.textContent = 'Заполните все поля';
        registrationMessage.style.display = 'block';
    }
});

// Закрытие модального окна при нажатии на кнопку "Закрыть"
closeModal.addEventListener('click', () => {
    registerModal.style.display = 'none';
});


// Выбор категории и выделение
document.querySelectorAll('.category').forEach(category => {
    category.addEventListener('click', (event) => {
        const selectedCategory = event.target.dataset.category;
        loadProducts(selectedCategory);

        document.querySelectorAll('.category').forEach(button => button.classList.remove('active'));
        event.target.classList.add('active');
    });
});

// Продукты по категориям
const productsByCategory = {
    toys: [
        { id: 1, name: "Мяч", price: 500, image: 'ball.jpg' },
        { id: 2, name: "Кукла", price: 700, image: 'doll.jpg' },
        // Добавьте остальные товары...
    ],
    clothes: [
        { id: 7, name: "Футболка", price: 1000, image: 'tshirt.jpg' },
        { id: 8, name: "Джинсы", price: 1500, image: 'jeans.jpg' },
        // Добавьте остальные товары...
    ],
    food: [
        { id: 13, name: "Хлеб", price: 100, image: 'bread.jpg' },
        { id: 14, name: "Молоко", price: 50, image: 'milk.jpg' },
        // Добавьте остальные товары...
    ]
};

// Загрузка продуктов
function loadProducts(category) {
    productsContainer.innerHTML = '';

    const products = productsByCategory[category];
    products.forEach(product => {
        const productDiv = document.createElement('div');
        productDiv.className = 'product';
        productDiv.innerHTML = `
            <img src="${product.image}" alt="${product.name}">
            <h3>${product.name}</h3>
            <p>Цена: ${product.price} руб.</p>
            <input type="number" id="quantity-${product.id}" value="1" min="1">
            <button onclick="addToCart(${product.id})">Добавить в корзину</button>
        `;
        productsContainer.appendChild(productDiv);
    });
}

// Добавление товара в корзину
function addToCart(productId) {
    const product = Object.values(productsByCategory).flat().find(p => p.id === productId);
    const quantityInput = document.getElementById(`quantity-${product.id}`);
    const quantity = parseInt(quantityInput.value);

    const cartItem = { ...product, quantity };

    const existingItem = cart.find(item => item.id === product.id);
    if (existingItem) {
        existingItem.quantity += quantity;
    } else {
        cart.push(cartItem);
    }

    cartCount.textContent = cart.reduce((total, item) => total + item.quantity, 0);
}

// Загрузка товаров в корзине
function loadCart() {
    cartItemsContainer.innerHTML = '';

    if (cart.length === 0) {
        cartItemsContainer.innerHTML = '<p>Корзина пуста</p>';
        return;
    }

    cart.forEach(item => {
        const itemDiv = document.createElement('div');
        itemDiv.innerHTML = `
            <h4>${item.name} x ${item.quantity}</h4>
            <p>Цена: ${item.price} руб. (Итого: ${item.price * item.quantity} руб.)</p>
        `;
        cartItemsContainer.appendChild(itemDiv);
    });
}

// Оформление заказа
document.getElementById('checkout').addEventListener('click', () => {
    if (cart.length === 0) {
        alert("Ваша корзина пуста. Добавьте товары перед оформлением заказа.");
    } else {
        orderMessage.textContent = 'Ваш заказ успешно оформлен!';
        orderMessage.style.display = 'block';

        cart = [];
        cartCount.textContent = '0';
        loadCart();
    }
});
