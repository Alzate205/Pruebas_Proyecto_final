import pytest
from playwright.sync_api import Page, expect
import subprocess
import time
import os
from pathlib import Path
import sys


def kill_process_on_port(port):
    """Mata cualquier proceso usando el puerto especificado (Windows)"""
    if sys.platform == "win32":
        try:
            subprocess.run(
                f'netstat -ano | findstr :{port}',
                shell=True,
                capture_output=True,
                text=True,
                check=False
            )
            subprocess.run(
                f'for /f "tokens=5" %a in (\'netstat -ano ^| findstr :{port}\') do taskkill /F /PID %a',
                shell=True,
                capture_output=True,
                check=False
            )
        except Exception:
            pass


@pytest.fixture(scope="module")
def backend_server():
    # Matar procesos previos en el puerto 8000
    kill_process_on_port(8000)
    time.sleep(1)

    # Obtener ruta al ejecutable de Python del entorno virtual
    if sys.platform == "win32":
        python_exe = Path(sys.executable).parent.parent / ".venv" / "Scripts" / "python.exe"
        if not python_exe.exists():
            # Si no encuentra el .venv, usa el Python actual
            python_exe = Path(sys.executable)
    else:
        python_exe = Path(sys.executable)

    # Iniciar servidor backend
    env = os.environ.copy()
    process = subprocess.Popen(
        [str(python_exe), "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    time.sleep(4)
    yield

    # Terminar proceso
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()

    time.sleep(1)


@pytest.fixture(scope="module")
def frontend_server():
    # Matar procesos previos en el puerto 3000
    kill_process_on_port(3000)
    time.sleep(1)
    
    # Obtener ruta absoluta al frontend
    current_dir = Path(__file__).resolve().parent
    frontend_path = current_dir.parent.parent.parent.parent / "frontend"
    
    # Iniciar servidor frontend
    process = subprocess.Popen(
        ["python", "-m", "http.server", "3000"],
        cwd=str(frontend_path),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    time.sleep(2)
    yield
    
    # Terminar proceso
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()


@pytest.fixture(scope="function")
def clean_database():
    """Limpia la base de datos antes de cada test"""
    # Esperar un momento antes de limpiar para asegurar que conexiones previas se cierren
    time.sleep(0.5)

    db_path = Path("inventory.db")

    # Intentar eliminar la base de datos si existe
    max_attempts = 10
    for attempt in range(max_attempts):
        try:
            if db_path.exists():
                db_path.unlink()
                print(f"Database deleted successfully on attempt {attempt + 1}")
            break
        except PermissionError:
            if attempt < max_attempts - 1:
                time.sleep(0.5)
            else:
                # Si no se puede eliminar después de varios intentos, advertir
                print(f"Warning: Could not delete database after {max_attempts} attempts")
                time.sleep(1)

    yield



def test_complete_flow(page: Page, backend_server, frontend_server, clean_database):
    # Navegar a la aplicación
    page.goto("http://localhost:3000")
    
    # Esperar que cargue
    page.wait_for_timeout(1500)
    
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
    page.wait_for_timeout(1500)
    
    # 3. Verificar que el producto aparece en el listado
    products_table = page.locator("#productsTable")
    expect(products_table).to_contain_text("Laptop Dell")
    expect(products_table).to_contain_text("Laptop Dell Inspiron 15")
    expect(products_table).to_contain_text("799.99")
    expect(products_table).to_contain_text("15")
    expect(products_table).to_contain_text("Electrónica")


def test_update_product(page: Page, backend_server, frontend_server, clean_database):
    page.goto("http://localhost:3000")
    page.wait_for_timeout(1500)
    
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
    page.wait_for_timeout(1500)
    
    # Editar producto - usar un selector más específico
    page.locator("button:text('Editar')").first.click()
    page.wait_for_timeout(500)
    
    page.fill("#productPrice", "175.00")
    page.fill("#productStock", "8")
    page.click("#submitBtn")
    page.wait_for_timeout(1500)
    
    # Verificar actualización
    expect(page.locator("#productsTable")).to_contain_text("175")
    expect(page.locator("#productsTable")).to_contain_text("8")


def test_delete_product(page: Page, backend_server, frontend_server, clean_database):
    page.goto("http://localhost:3000")
    page.wait_for_timeout(1500)
    
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
    page.wait_for_timeout(1500)
    
    # Verificar que el producto está antes de eliminar
    expect(page.locator("#productsTable")).to_contain_text("Balón")

    # Configurar handler para el diálogo ANTES de hacer clic
    page.on("dialog", lambda dialog: dialog.accept())

    # Eliminar producto - buscar la fila que contiene "Balón" y hacer clic en su botón eliminar
    # Primero, encontrar la fila que contiene "Balón"
    balon_row = page.locator("tr:has-text('Balón de fútbol')").first
    # Luego hacer clic en el botón eliminar dentro de esa fila
    balon_row.locator("button.btn-delete").click()
    page.wait_for_timeout(2000)

    # Verificar que ya no está
    expect(page.locator("#productsTable")).not_to_contain_text("Balón")