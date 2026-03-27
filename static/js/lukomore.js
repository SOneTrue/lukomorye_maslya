let cart = [];
let cartCount = 0;

function addToCart(name, price) {
    cart.push({ name, price });
    cartCount++;
    updateCartDisplay();
    showToast(`✅ ${name} добавлен в корзину!`);
}

function updateCartDisplay() {
    document.getElementById('cartCount').textContent = cartCount;
    const cartItems = document.getElementById('cartItems');

    if (cart.length === 0) {
        cartItems.innerHTML = '<p class="text-center text-muted">🛒 Корзина пуста</p>';
    } else {
        const grouped = {};
        cart.forEach(item => {
            grouped[item.name]
                ? grouped[item.name].quantity++
                : (grouped[item.name] = { ...item, quantity: 1 });
        });
        cartItems.innerHTML = Object.entries(grouped).map(([, item]) => `
            <div class="d-flex justify-content-between align-items-center p-3"
                 style="border-bottom: 2px dashed #ffcc80;">
                <div>
                    <strong style="color: var(--dark-color);">${item.name}</strong><br>
                    <small style="color: #90a4ae;">${item.price.toLocaleString()} ₽ × ${item.quantity}</small>
                </div>
                <span style="font-weight:800;color:#ff6b35;">
                    ${(item.price * item.quantity).toLocaleString()} ₽
                </span>
            </div>
        `).join('');
    }

    const total = cart.reduce((sum, i) => sum + i.price, 0);
    document.getElementById('cartTotal').textContent = total.toLocaleString() + ' ₽';
}

function showToast(message) {
    const container = document.getElementById('toastContainer');
    const id = 'toast-' + Date.now();
    container.insertAdjacentHTML('beforeend', `
        <div id="${id}" class="toast show toast-custom" role="alert">
            <div class="toast-header toast-header-custom">
                <i class="bi bi-check-circle-fill me-2"></i>
                <strong class="me-auto">Успешно</strong>
                <button type="button" class="btn-close btn-close-white"
                        onclick="removeToast('${id}')"></button>
            </div>
            <div class="toast-body" style="font-weight:600;">${message}</div>
        </div>
    `);
    setTimeout(() => removeToast(id), 3000);
}

function removeToast(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}

function checkout() {
    if (cart.length === 0) { showToast('⚠️ Корзина пуста!'); return; }
    const total = cart.reduce((sum, i) => sum + i.price, 0);
    alert(`🎉 Спасибо за заказ!\n\nСумма: ${total.toLocaleString()} ₽\n\nМенеджер свяжется с вами.`);
    cart = []; cartCount = 0;
    updateCartDisplay();
    bootstrap.Modal.getInstance(document.getElementById('cartModal')).hide();
}

// Открытие корзины
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('cartBtn').addEventListener('click', () => {
        updateCartDisplay();
        new bootstrap.Modal(document.getElementById('cartModal')).show();
    });

    // Плавный скролл
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const target = document.querySelector(a.getAttribute('href'));
            if (target) { e.preventDefault(); target.scrollIntoView({ behavior: 'smooth' }); }
        });
    });
});