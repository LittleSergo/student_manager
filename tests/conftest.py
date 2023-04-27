import pytest

from sqlalchemy import create_engine
from app import create_app


@pytest.fixture
def app():
    app = create_app({
        "TESTING": True,
        "DATABASE": create_engine("sqlite+pysqlite:///:memory:",
                                  echo=False)
    })

    with app.app_context():
        from db import init_db
        init_db()
        yield app


@pytest.fixture
def client(app):
    yield app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
