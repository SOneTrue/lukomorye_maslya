let cart = [];

function saveCart() {
    localStorage.setItem("cart", JSON.stringify(cart));
    updateCartCount();
    renderCartPage();
}

function loadCart() {
    const saved = localStorage.getItem("cart");
    cart = saved ? JSON.parse(saved) : [];
    updateCartCount();
    renderCartPage();
}

function updateCartCount() {
    const count = cart.reduce((sum, item) => sum + item.quantity, 0);
    const badge = document.getElementById("cartCount");
    if (badge) badge.textContent = count;
}

function addToCart(id, name, price, image = "") {
    id = Number(id);
    price = Number(price);

    const existing = cart.find(item => item.id === id);

    if (existing) {
        existing.quantity += 1;
    } else {
        cart.push({
            id,
            name,
            price,
            image,
            quantity: 1
        });
    }

    saveCart();
    showToast(`✅ ${name} добавлен в корзину!`);
}

function removeFromCart(id) {
    id = Number(id);
    cart = cart.filter(item => item.id !== id);
    saveCart();
}

function changeQuantity(id, delta) {
    id = Number(id);
    const item = cart.find(item => item.id === id);
    if (!item) return;

    item.quantity += delta;

    if (item.quantity <= 0) {
        removeFromCart(id);
        return;
    }

    saveCart();
}

function renderCartPage() {
    const cartItems = document.getElementById("cartPageItems");
    const cartCount = document.getElementById("cartPageCount");

    if (!cartItems) return;

    if (cart.length === 0) {
        cartItems.innerHTML = `
            <div class="text-center text-muted py-5">
                <i class="bi bi-basket" style="font-size:3rem;"></i>
                <p class="mt-3 mb-0">Корзина пуста</p>
            </div>
        `;
        if (cartCount) cartCount.textContent = "0";
        return;
    }

    cartItems.innerHTML = cart.map(item => `
        <div class="d-flex justify-content-between align-items-center p-3 mb-3 rounded-4"
             style="border:1px solid #eee;background:#fffaf5;">
            <div>
                <strong style="color: var(--dark-color);">${item.name}</strong><br>
                <small style="color: #90a4ae;">${item.price.toLocaleString()} ₽ × ${item.quantity}</small>
            </div>
            <div class="text-end">
                <div class="mb-2" style="font-weight:800;color:#ff6b35;">
                    ${(item.price * item.quantity).toLocaleString()} ₽
                </div>
                <div class="d-flex align-items-center gap-2 justify-content-end">
                    <button class="btn btn-sm btn-outline-secondary" onclick="changeQuantity(${item.id}, -1)">−</button>
                    <span style="min-width:24px;text-align:center;">${item.quantity}</span>
                    <button class="btn btn-sm btn-outline-secondary" onclick="changeQuantity(${item.id}, 1)">+</button>
                    <button class="btn btn-sm btn-outline-danger ms-2" onclick="removeFromCart(${item.id})">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `).join("");

    const totalCount = cart.reduce((sum, item) => sum + item.quantity, 0);
    if (cartCount) cartCount.textContent = totalCount;
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function submitCartOrder() {
    if (cart.length === 0) {
        showToast("⚠️ Корзина пуста!");
        return;
    }

    const customerName = document.getElementById("customerName")?.value.trim();
    const customerPhone = document.getElementById("customerPhone")?.value.trim();
    const customerComment = document.getElementById("customerComment")?.value.trim() || "";

    if (!customerName || !customerPhone) {
        showToast("Укажите имя и телефон.");
        return;
    }

    fetch("/order/create/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            customer_name: customerName,
            phone: customerPhone,
            comment: customerComment,
            items: cart.map(item => ({
                id: item.id,
                quantity: item.quantity
            }))
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert(
                `✅ Заказ оформлен!\n\n` +
                `Номер заказа: ${data.order_number}\n\n` +
                `Сохраните этот номер и назовите его в магазине при получении.`
            );

            cart = [];
            saveCart();

            const nameInput = document.getElementById("customerName");
            const phoneInput = document.getElementById("customerPhone");
            const commentInput = document.getElementById("customerComment");

            if (nameInput) nameInput.value = "";
            if (phoneInput) phoneInput.value = "";
            if (commentInput) commentInput.value = "";
        } else {
            showToast(data.message || "Ошибка оформления заказа");
        }
    })
    .catch(() => {
        showToast("Ошибка соединения с сервером");
    });
}

function showToast(message) {
    const container = document.getElementById("toastContainer");
    if (!container) {
        alert(message);
        return;
    }

    const id = "toast-" + Date.now();
    container.insertAdjacentHTML("beforeend", `
        <div id="${id}" class="toast show toast-custom" role="alert">
            <div class="toast-header toast-header-custom">
                <i class="bi bi-check-circle-fill me-2"></i>
                <strong class="me-auto">Уведомление</strong>
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

document.addEventListener("DOMContentLoaded", () => {
    loadCart();

    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener("click", e => {
            const target = document.querySelector(a.getAttribute("href"));
            if (target) {
                e.preventDefault();
                target.scrollIntoView({ behavior: "smooth" });
            }
        });
    });
});