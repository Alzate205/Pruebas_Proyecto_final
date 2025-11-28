from fastapi import FastAPI
from .database import Base, engine
from . import models
from .api import categories, products

# Crear tablas en BD
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Inventory API")

app.include_router(categories.router, prefix="/api")
app.include_router(products.router, prefix="/api")
