
const API = {
    products: "/api/products/",
    login: "/api/auth/login",
    register: "/api/auth/register",
    me: "/api/auth/me",
    logout: "/api/auth/logout",
    cart: "/api/cart/",
    checkout: "/api/orders/checkout",
    orders: "/api/orders/"
};

let currentUser = null;
let products = [];

const $ = (id) => document.getElementById(id);

// API request handler
async function api(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    let data = {};

    try {
        data = await response.json();
    } catch (_) {}

    if (!response.ok) {
        throw new Error(
            data.error || data.message || `Request failed (${response.status})`
        );
    }

    return data;
}

// Notifications
function toast(message) {
    const el = $("toast");

    el.textContent = message;
    el.classList.add("show");

    setTimeout(() => {
        el.classList.remove("show");
    }, 2800);
}

// Currency formatting
function money(value) {
    return new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR",
        maximumFractionDigits: 2
    }).format(value);
}

// Prevent HTML injection
function escapeHTML(value) {
    return String(value ?? "").replace(/[&<>"']/g, char => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[char]);
}

// Load products
async function loadProducts() {
    const grid = $("productGrid");

    grid.innerHTML = "<p>Loading products...</p>";

    try {
        const data = await api(API.products);

        products = data.products || [];

        renderProducts(products);

    } catch (error) {
        console.error("Product loading error:", error);

        grid.innerHTML = `
            <p>Unable to load products.</p>
            <button class="primary-btn" onclick="loadProducts()">
                Try Again
            </button>
        `;
    }
}

// Render product cards
function renderProducts(items) {
    $("productCount").textContent = `${items.length} products`;

    if (!items.length) {
        $("productGrid").innerHTML = "<p>No products found.</p>";
        return;
    }

    $("productGrid").innerHTML = items.map(product => {

        // Ignore placeholder image URLs
        const validImage =
            product.image_url &&
            !product.image_url.includes("example.com");

        return `
            <article class="product-card">

                <div class="product-image">

                    ${
                        validImage
                        ? `
                            <img
                                src="${escapeHTML(product.image_url)}"
                                alt="${escapeHTML(product.name)}"
                                loading="lazy"
                                onerror="
                                    this.style.display='none';
                                    this.nextElementSibling.style.display='block';
                                "
                            >
                        `
                        : ""
                    }

                    <span
                        class="product-placeholder"
                        style="${validImage ? "display:none" : ""}"
                    >
                        🛍️
                    </span>

                </div>

                <div class="product-info">

                    <h3>${escapeHTML(product.name)}</h3>

                    <p class="product-description">
                        ${escapeHTML(
                            product.description ||
                            "Discover this product at CloudCart."
                        )}
                    </p>

                    <div class="product-bottom">

                        <span class="price">
                            ${money(product.price)}
                        </span>

                        <button
                            class="add-btn"
                            data-add="${product.id}"
                            ${product.stock < 1 ? "disabled" : ""}
                        >
                            ${product.stock < 1 ? "Out of stock" : "Add +"}
                        </button>

                    </div>

                    <p class="quantity">
                        ${product.stock} available
                    </p>

                </div>

            </article>
        `;
    }).join("");

    document.querySelectorAll("[data-add]").forEach(button => {
        button.addEventListener("click", () => {
            addToCart(Number(button.dataset.add));
        });
    });
}

// Check current login session
async function checkSession() {
    try {
        const data = await api(API.me);

        currentUser = data.user || data;

        updateAuthUI();

    } catch (_) {
        currentUser = null;
        updateAuthUI();
    }
}

// Update login/logout buttons
function updateAuthUI() {
    $("loginBtn").classList.toggle("hidden", !!currentUser);
    $("logoutBtn").classList.toggle("hidden", !currentUser);
}

// Open authentication modal
function openAuth(mode = "login") {
    $("authModal").classList.remove("hidden");
    setAuthMode(mode);
}

// Switch login/register mode
function setAuthMode(mode) {
    const register = mode === "register";

    $("authTitle").textContent =
        register ? "Create Account" : "Login";

    $("authSubmit").textContent =
        register ? "Create Account" : "Login";

    $("usernameField").classList.toggle("hidden", !register);
    $("username").required = register;

    $("switchAuth").innerHTML = register
        ? 'Already have an account? <button type="button">Login</button>'
        : 'New here? <button type="button">Create account</button>';

    $("switchAuth").querySelector("button").addEventListener(
        "click",
        () => setAuthMode(register ? "login" : "register"),
        { once: true }
    );

    $("authForm").dataset.mode = mode;
}

// Login and registration
$("authForm").addEventListener("submit", async event => {
    event.preventDefault();

    const register =
        $("authForm").dataset.mode === "register";

    const payload = {
        email: $("email").value.trim(),
        password: $("password").value
    };

    if (register) {
        payload.username = $("username").value.trim();
    }

    try {
        const data = await api(
            register ? API.register : API.login,
            {
                method: "POST",
                body: JSON.stringify(payload)
            }
        );

        if (register) {
            toast("Account created. Please log in.");
            setAuthMode("login");
        } else {
            currentUser = data.user || data;

            $("authModal").classList.add("hidden");

            updateAuthUI();

            toast("Welcome to CloudCart!");

            await loadCart();
        }

    } catch (error) {
        toast(error.message);
    }
});

// Add product to cart
async function addToCart(productId) {
    if (!currentUser) {
        openAuth("login");
        toast("Please log in to add items.");
        return;
    }

    try {
        await api(API.cart, {
            method: "POST",
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });

        toast("Added to your cart!");

        await loadCart();

    } catch (error) {
        toast(error.message);
    }
}

// Load cart
async function loadCart() {
    if (!currentUser) {
        $("cartCount").textContent = "0";
        return;
    }

    try {
        const data = await api(API.cart);

        $("cartCount").textContent = data.count || 0;

        $("cartItems").innerHTML =
            (data.items || []).map(item => `
                <div class="cart-row">

                    <div>
                        <strong>
                            ${escapeHTML(item.product.name)}
                        </strong>

                        <div class="quantity">
                            ${money(item.product.price)} × ${item.quantity}
                        </div>
                    </div>

                    <strong>${money(item.subtotal)}</strong>

                    <button
                        class="remove-btn"
                        data-remove="${item.id}"
                    >
                        Remove
                    </button>

                </div>
            `).join("") || "<p>Your cart is empty.</p>";

        $("cartTotal").textContent =
            money(data.total || 0);

        document.querySelectorAll("[data-remove]").forEach(button => {
            button.addEventListener("click", () => {
                removeCartItem(Number(button.dataset.remove));
            });
        });

    } catch (error) {
        console.error("Cart loading error:", error);
        toast(error.message);
    }
}

// Remove cart item
async function removeCartItem(id) {
    try {
        await api(`${API.cart}${id}`, {
            method: "DELETE"
        });

        await loadCart();

        toast("Item removed.");

    } catch (error) {
        toast(error.message);
    }
}

// Checkout
async function checkout() {
    if (!currentUser) {
        openAuth("login");
        return;
    }

    if (!confirm("Place your order now?")) {
        return;
    }

    try {
        const data = await api(API.checkout, {
            method: "POST"
        });

        toast(`Order #${data.order.id} placed successfully!`);

        await loadCart();
        await loadProducts();
        await showOrders();

    } catch (error) {
        toast(error.message);
    }
}

// Order history
async function showOrders() {
    if (!currentUser) {
        openAuth("login");
        return;
    }

    try {
        const data = await api(API.orders);

        $("ordersList").innerHTML =
            (data.orders || []).map(order => `
                <div class="order-row">

                    <div>
                        <strong>Order #${order.id}</strong>

                        <div class="quantity">
                            ${new Date(order.created_at).toLocaleString()}
                        </div>

                        <div class="quantity">
                            ${order.items.length} item(s) ·
                            ${escapeHTML(order.status)}
                        </div>
                    </div>

                    <strong>
                        ${money(order.total_amount)}
                    </strong>

                </div>
            `).join("") ||
            "<p>You haven't placed any orders yet.</p>";

        $("ordersPanel").classList.remove("hidden");
        $("cartPanel").classList.add("hidden");

        $("ordersPanel").scrollIntoView({
            behavior: "smooth"
        });

    } catch (error) {
        toast(error.message);
    }
}

// Event listeners
$("loginBtn").addEventListener("click", () => {
    openAuth("login");
});

$("logoutBtn").addEventListener("click", async () => {
    try {
        await api(API.logout, {
            method: "POST"
        });

        currentUser = null;

        updateAuthUI();

        await loadCart();

        toast("Logged out.");

    } catch (error) {
        toast(error.message);
    }
});

$("closeModal").addEventListener("click", () => {
    $("authModal").classList.add("hidden");
});

$("cartBtn").addEventListener("click", async () => {
    if (!currentUser) {
        openAuth("login");
        return;
    }

    $("cartPanel").classList.remove("hidden");
    $("ordersPanel").classList.add("hidden");

    await loadCart();

    $("cartPanel").scrollIntoView({
        behavior: "smooth"
    });
});

$("closeCart").addEventListener("click", () => {
    $("cartPanel").classList.add("hidden");
});

$("ordersBtn").addEventListener("click", showOrders);

$("closeOrders").addEventListener("click", () => {
    $("ordersPanel").classList.add("hidden");
});

$("checkoutBtn").addEventListener("click", checkout);

// Search
function searchProducts() {
    const query =
        $("searchInput").value.toLowerCase().trim();

    const filtered = products.filter(product =>
        `${product.name} ${product.description || ""}`
            .toLowerCase()
            .includes(query)
    );

    renderProducts(filtered);
}

$("searchBtn").addEventListener("click", searchProducts);
$("searchInput").addEventListener("input", searchProducts);

// Initialize application
(async function init() {
    setAuthMode("login");

    await checkSession();

    await loadProducts();

    await loadCart();
})();
