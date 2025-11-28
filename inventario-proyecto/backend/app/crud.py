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
