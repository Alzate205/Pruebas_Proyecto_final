import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import os
import signal


@pytest.fixture(scope="module")
def backend_server():
    # Iniciar servidor backend
    env = os.environ.copy()
    process = subprocess.Popen(
        ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    time.sleep(3)
    yield
    os.kill(process.pid, signal.SIGTERM)
    process.wait()


@pytest.fixture(scope="module")
def frontend_server():
    # Iniciar servidor frontend
    process = subprocess.Popen(
        ["python", "-m", "http.server", "3000"],
        cwd="../../frontend",
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)
    yield
    os.kill(process.pid, signal.SIGTERM)
    process.wait()


def test_complete_flow(page: Page, backend_server, frontend_server):
    # Navegar a la aplicación
    page.goto("http://localhost:3000")
    
    # Esperar que cargue
    page.wait_for_timeout(1000)
    
    # 1. Crear categoría
    page.fill("#categoryName", "Electrónica")
    page.click("#categoryForm button[type='submit']")
    page.wait_for_timeout(1000)
    
    # Verificar que la categoría aparece en la tabla
    expect(page.locator("#categoriesTable")).to_contain_text("Electrónica")
    
    # 2. Crear producto
    page.fill("#productName", "Laptop Dell")
    page.fill("#productDescription", "Laptop Dell Inspiron 15")
    page.fill("#productPrice", "799.99")
    page.fill("#productStock", "15")
    page.select_option("#productCategory", label="Electrónica")
    page.click("#productForm button[type='submit']")
    page.wait_for_timeout(1000)
    
    # 3. Verificar que el producto aparece en el listado
    products_table = page.locator("#productsTable")
    expect(products_table).to_contain_text("Laptop Dell")
    expect(products_table).to_contain_text("Laptop Dell Inspiron 15")
    expect(products_table).to_contain_text("799.99")
    expect(products_table).to_contain_text("15")
    expect(products_table).to_contain_text("Electrónica")


def test_update_product(page: Page, backend_server, frontend_server):
    page.goto("http://localhost:3000")
    page.wait_for_timeout(1000)
    
    # Crear categoría y producto
    page.fill("#categoryName", "Hogar")
    page.click("#categoryForm button[type='submit']")
    page.wait_for_timeout(1000)
    
    page.fill("#productName", "Mesa")
    page.fill("#productDescription", "Mesa de madera")
    page.fill("#productPrice", "150.00")
    page.fill("#productStock", "5")
    page.select_option("#productCategory", label="Hogar")
    page.click("#productForm button[type='submit']")
    page.wait_for_timeout(1000)
    
    # Editar producto
    page.click("button:text('Editar')")
    page.wait_for_timeout(500)
    
    page.fill("#productPrice", "175.00")
    page.fill("#productStock", "8")
    page.click("#submitBtn")
    page.wait_for_timeout(1000)
    
    # Verificar actualización
    expect(page.locator("#productsTable")).to_contain_text("175")
    expect(page.locator("#productsTable")).to_contain_text("8")


def test_delete_product(page: Page, backend_server, frontend_server):
    page.goto("http://localhost:3000")
    page.wait_for_timeout(1000)
    
    # Crear categoría y producto
    page.fill("#categoryName", "Deportes")
    page.click("#categoryForm button[type='submit']")
    page.wait_for_timeout(1000)
    
    page.fill("#productName", "Balón")
    page.fill("#productDescription", "Balón de fútbol")
    page.fill("#productPrice", "25.00")
    page.fill("#productStock", "20")
    page.select_option("#productCategory", label="Deportes")
    page.click("#productForm button[type='submit']")
    page.wait_for_timeout(1000)
    
    # Eliminar producto
    page.on("dialog", lambda dialog: dialog.accept())
    page.click("button.btn-delete")
    page.wait_for_timeout(1000)
    
    # Verificar que ya no está
    expect(page.locator("#productsTable")).not_to_contain_text("Balón")