const API_URL = 'http://localhost:8000/api';

// Cargar categorías al iniciar
async function loadCategories() {
    const response = await fetch(`${API_URL}/categories/`);
    const categories = await response.json();
    
    const tableBody = document.getElementById('categoriesTable');
    tableBody.innerHTML = '';
    
    const select = document.getElementById('productCategory');
    select.innerHTML = '<option value="">Seleccione una categoría</option>';
    
    categories.forEach(cat => {
        const row = `<tr><td>${cat.id}</td><td>${cat.name}</td></tr>`;
        tableBody.innerHTML += row;
        
        const option = `<option value="${cat.id}">${cat.name}</option>`;
        select.innerHTML += option;
    });
}

// Cargar productos
async function loadProducts() {
    const response = await fetch(`${API_URL}/products/`);
    const products = await response.json();
    
    const tableBody = document.getElementById('productsTable');
    tableBody.innerHTML = '';
    
    products.forEach(prod => {
        const row = `
            <tr>
                <td>${prod.id}</td>
                <td>${prod.name}</td>
                <td>${prod.description}</td>
                <td>$${prod.price}</td>
                <td>${prod.stock}</td>
                <td>${prod.category.name}</td>
                <td class="actions">
                    <button onclick="editProduct(${prod.id}, '${prod.name}', '${prod.description}', ${prod.price}, ${prod.stock}, ${prod.category_id})">Editar</button>
                    <button class="btn-delete" onclick="deleteProduct(${prod.id})">Eliminar</button>
                </td>
            </tr>
        `;
        tableBody.innerHTML += row;
    });
}

// Crear categoría
document.getElementById('categoryForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const name = document.getElementById('categoryName').value;
    
    await fetch(`${API_URL}/categories/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name })
    });
    
    document.getElementById('categoryName').value = '';
    loadCategories();
});

// Crear o actualizar producto
document.getElementById('productForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const productId = document.getElementById('productId').value;
    const data = {
        name: document.getElementById('productName').value,
        description: document.getElementById('productDescription').value,
        price: parseFloat(document.getElementById('productPrice').value),
        stock: parseInt(document.getElementById('productStock').value),
        category_id: parseInt(document.getElementById('productCategory').value)
    };
    
    if (productId) {
        await fetch(`${API_URL}/products/${productId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    } else {
        await fetch(`${API_URL}/products/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });
    }
    
    document.getElementById('productForm').reset();
    document.getElementById('productId').value = '';
    document.getElementById('submitBtn').textContent = 'Crear Producto';
    document.getElementById('cancelBtn').style.display = 'none';
    loadProducts();
});

// Editar producto
function editProduct(id, name, description, price, stock, category_id) {
    document.getElementById('productId').value = id;
    document.getElementById('productName').value = name;
    document.getElementById('productDescription').value = description;
    document.getElementById('productPrice').value = price;
    document.getElementById('productStock').value = stock;
    document.getElementById('productCategory').value = category_id;
    document.getElementById('submitBtn').textContent = 'Actualizar Producto';
    document.getElementById('cancelBtn').style.display = 'inline-block';
}

// Cancelar edición
document.getElementById('cancelBtn').addEventListener('click', () => {
    document.getElementById('productForm').reset();
    document.getElementById('productId').value = '';
    document.getElementById('submitBtn').textContent = 'Crear Producto';
    document.getElementById('cancelBtn').style.display = 'none';
});

// Eliminar producto
async function deleteProduct(id) {
    if (confirm('¿Estás seguro de eliminar este producto?')) {
        await fetch(`${API_URL}/products/${id}`, { method: 'DELETE' });
        loadProducts();
    }
}

// Cargar datos al iniciar
loadCategories();
loadProducts();