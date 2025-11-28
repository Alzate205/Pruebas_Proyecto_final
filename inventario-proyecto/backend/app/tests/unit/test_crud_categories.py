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


def test_create_category_ok():
    db_gen = get_test_db()
    db = next(db_gen)

    category_in = schemas.CategoryCreate(name="Ropa")
    category = crud.create_category(db, category_in)

    assert category.id is not None
    assert category.name == "Ropa"
