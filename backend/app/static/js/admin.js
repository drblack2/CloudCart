const $ = (id) => document.getElementById(id);

const money = (amount) =>
    new Intl.NumberFormat("en-IN", {
        style: "currency",
        currency: "INR"
    }).format(Number(amount || 0));

async function api(url, options = {}) {
    const response = await fetch(url, {
        credentials: "same-origin",
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {})
        }
    });

    const data = await response.json().catch(() => ({}));

    if (!response.ok) {
        throw new Error(data.error || `Request failed: ${response.status}`);
    }

    return data;
}

function notify(message) {
    const box = $("message");
    box.textContent = message;
    box.style.display = "block";

    setTimeout(() => {
        box.style.display = "none";
    }, 3000);
}

async function loadDashboard() {
    const data = await api("/api/admin/dashboard");

    $("totalProducts").textContent = data.total_products;
    $("totalOrders").textContent = data.total_orders;
    $("totalCustomers").textContent = data.total_customers;
    $("revenue").textContent = money(data.total_revenue);
    $("lowStock").textContent = data.low_stock;
}

async function loadProducts() {
    const data = await api("/api/products/");
    const table = $("productTable");

    table.innerHTML = "";

    data.products.forEach((product) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${product.id}</td>
            <td>${escapeHtml(product.name)}</td>
            <td>${money(product.price)}</td>
            <td>${product.stock}</td>
            <td>
                <button data-edit="${product.id}">Edit</button>
                <button class="danger" data-delete="${product.id}">Delete</button>
            </td>
        `;

        table.appendChild(row);
    });
}

async function loadOrders() {
    const data = await api("/api/admin/orders");
    const table = $("orderTable");

    table.innerHTML = "";

    data.orders.forEach((order) => {
        const customer = order.customer
            ? order.customer.username
            : `User ${order.user_id}`;

        const row = document.createElement("tr");

        row.innerHTML = `
            <td>#${order.id}</td>
            <td>${escapeHtml(customer)}</td>
            <td>${money(order.total_amount)}</td>
            <td>${escapeHtml(order.status)}</td>
            <td>
                <select data-status="${order.id}">
                    ${["placed", "processing", "shipped", "delivered", "cancelled"]
                        .map(status => `
                            <option value="${status}" ${status === order.status ? "selected" : ""}>
                                ${status}
                            </option>
                        `).join("")}
                </select>
                <button data-update-order="${order.id}">Save</button>
            </td>
        `;

        table.appendChild(row);
    });
}

async function loadCustomers() {
    const data = await api("/api/admin/customers");
    const table = $("customerTable");

    table.innerHTML = "";

    data.customers.forEach((customer) => {
        const row = document.createElement("tr");

        row.innerHTML = `
            <td>${customer.id}</td>
            <td>${escapeHtml(customer.username)}</td>
            <td>${escapeHtml(customer.email)}</td>
            <td>${new Date(customer.created_at).toLocaleDateString()}</td>
        `;

        table.appendChild(row);
    });
}

function escapeHtml(value) {
    return String(value ?? "").replace(/[&<>"']/g, (character) => ({
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;",
        '"': "&quot;",
        "'": "&#39;"
    })[character]);
}

function clearProductForm() {
    $("productId").value = "";
    $("productName").value = "";
    $("productPrice").value = "";
    $("productStock").value = "";
    $("productImage").value = "";
    $("productDescription").value = "";
}

function showProductForm(product = null) {
    $("productForm").classList.remove("hidden");

    if (product) {
        $("productId").value = product.id;
        $("productName").value = product.name;
        $("productPrice").value = product.price;
        $("productStock").value = product.stock;
        $("productImage").value = product.image_url || "";
        $("productDescription").value = product.description || "";
    } else {
        clearProductForm();
    }

    $("productName").focus();
}

async function saveProduct() {
    const id = $("productId").value;

    const payload = {
        name: $("productName").value.trim(),
        price: Number($("productPrice").value),
        stock: Number($("productStock").value),
        image_url: $("productImage").value.trim() || null,
        description: $("productDescription").value.trim()
    };

    if (!payload.name || !Number.isFinite(payload.price) ||
        payload.price <= 0 || !Number.isInteger(payload.stock) ||
        payload.stock < 0) {
        notify("Enter a valid name, positive price, and non-negative stock.");
        return;
    }

    await api(id ? `/api/products/${id}` : "/api/products/", {
        method: id ? "PUT" : "POST",
        body: JSON.stringify(payload)
    });

    $("productForm").classList.add("hidden");
    clearProductForm();

    await Promise.all([loadProducts(), loadDashboard()]);
    notify(id ? "Product updated" : "Product added");
}

async function editProduct(id) {
    const data = await api(`/api/products/${id}`);
    showProductForm(data.product);
}

async function deleteProduct(id) {
    if (!confirm(`Delete product #${id}?`)) return;

    await api(`/api/products/${id}`, { method: "DELETE" });

    await Promise.all([loadProducts(), loadDashboard()]);
    notify("Product deleted");
}

async function updateOrder(id) {
    const status = document.querySelector(`[data-status="${id}"]`).value;

    await api(`/api/admin/orders/${id}/status`, {
        method: "PATCH",
        body: JSON.stringify({ status })
    });

    await Promise.all([loadOrders(), loadDashboard()]);
    notify("Order status updated");
}

$("addProductBtn").addEventListener("click", () => showProductForm());
$("saveProductBtn").addEventListener("click", () => {
    saveProduct().catch(error => notify(error.message));
});

$("cancelProductBtn").addEventListener("click", () => {
    $("productForm").classList.add("hidden");
    clearProductForm();
});

$("productTable").addEventListener("click", (event) => {
    const editId = event.target.dataset.edit;
    const deleteId = event.target.dataset.delete;

    if (editId) {
        editProduct(editId).catch(error => notify(error.message));
    }

    if (deleteId) {
        deleteProduct(deleteId).catch(error => notify(error.message));
    }
});

$("orderTable").addEventListener("click", (event) => {
    const orderId = event.target.dataset.updateOrder;

    if (orderId) {
        updateOrder(orderId).catch(error => notify(error.message));
    }
});

$("logoutBtn").addEventListener("click", async () => {
    try {
        await api("/api/auth/logout", { method: "POST" });
        window.location.href = "/";
    } catch (error) {
        notify(error.message);
    }
});

async function init() {
    try {
        const session = await api("/api/auth/me");
        $("adminName").textContent = session.user.username;

        if (session.user.role !== "admin") {
            window.location.href = "/";
            return;
        }

        await Promise.all([
            loadDashboard(),
            loadProducts(),
            loadOrders(),
            loadCustomers()
        ]);
    } catch (error) {
        notify(error.message);
    }
}

init();

