from sqlalchemy.orm import Session
from . import models, schemas


# CATEGORIES
def create_category(db: Session, category_in: schemas.CategoryCreate) -> models.Category:
    db_category = models.Category(name=category_in.name)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_categories(db: Session):
    return db.query(models.Category).all()


def get_category(db: Session, category_id: int):
    return db.query(models.Category).filter(models.Category.id == category_id).first()


# PRODUCTS
def create_product(db: Session, product_in: schemas.ProductCreate) -> models.Product:
    # Validar que exista categoría
    category = get_category(db, product_in.category_id)
    if not category:
        raise ValueError("Category not found")

    db_product = models.Product(
        name=product_in.name,
        description=product_in.description,
        price=product_in.price,
        stock=product_in.stock,
        category_id=product_in.category_id,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_products(db: Session):
    return db.query(models.Product).all()

def update_product(db: Session, product_id: int, product_in: schemas.ProductCreate) -> models.Product:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise ValueError("Product not found")
    
    # Validar categoría
    category = get_category(db, product_in.category_id)
    if not category:
        raise ValueError("Category not found")
    
    db_product.name = product_in.name
    db_product.description = product_in.description
    db_product.price = product_in.price
    db_product.stock = product_in.stock
    db_product.category_id = product_in.category_id
    
    db.commit()
    db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise ValueError("Product not found")
    
    db.delete(db_product)
    db.commit()
    return True