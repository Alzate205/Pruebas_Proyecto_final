from pydantic import BaseModel, Field, ConfigDict


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=1)


class CategoryCreate(CategoryBase):
    pass


class Category(CategoryBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class ProductBase(BaseModel):
    name: str
    description: str
    price: float
    stock: int
    category_id: int


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
    category: Category

    model_config = ConfigDict(from_attributes=True)