import pytest
from playwright.sync_api import sync_playwright
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app import models


# Database setup for integration tests
engine = create_engine(
    "sqlite:///file:memdb1?mode=memory&cache=shared&uri=true",
    connect_args={"check_same_thread": False},
    poolclass=None  # Disable connection pooling for tests
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """TestClient fixture for integration tests"""
    # Create tables before each test
    Base.metadata.create_all(bind=engine)

    # Override the database dependency
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    # Clean up
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


# Playwright fixtures for E2E tests
@pytest.fixture(scope="session")
def playwright():
    with sync_playwright() as p:
        yield p


@pytest.fixture(scope="function")
def page(playwright):
    browser = playwright.chromium.launch(
        headless=True,
        args=['--no-sandbox', '--disable-dev-shm-usage']
    )
    context = browser.new_context(
        viewport={'width': 1280, 'height': 720},
        ignore_https_errors=True
    )
    page = context.new_page()
    yield page
    context.close()
    browser.close()