from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from app import crud, schemas


def get_test_db():
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def test_create_product_ok():
    db_gen = get_test_db()
    db = next(db_gen)
    
    # Primero crear categoría
    category_in = schemas.CategoryCreate(name="Tecnología")
    category = crud.create_category(db, category_in)
    
    # Crear producto
    product_in = schemas.ProductCreate(
        name="Mouse",
        description="Mouse inalámbrico",
        price=25.0,
        stock=50,
        category_id=category.id
    )
    product = crud.create_product(db, product_in)
    
    assert product.id is not None
    assert product.name == "Mouse"
    assert product.price == 25.0


def test_create_product_invalid_category():
    db_gen = get_test_db()
    db = next(db_gen)
    
    product_in = schemas.ProductCreate(
        name="Producto",
        description="Descripción",
        price=10.0,
        stock=5,
        category_id=999
    )
    
    try:
        crud.create_product(db, product_in)
        assert False, "Debería lanzar ValueError"
    except ValueError as e:
        assert str(e) == "Category not found"