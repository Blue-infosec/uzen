from starlette.config import environ
from starlette.testclient import TestClient
from tortoise import Tortoise, run_async
from tortoise.contrib.test import finalizer, initializer
import os
import pytest

# This line would raise an error if we use it after 'settings' has been imported.
environ["TESTING"] = "TRUE"

from uzen import settings  # noqa
from uzen import create_app  # noqa


@pytest.fixture(scope="session", autouse=True)
def initialize_tests(request):
    db_url = environ.get("TORTOISE_TEST_DB", "sqlite://:memory:")
    initializer(settings.APP_MODELS, db_url=db_url)
    request.addfinalizer(finalizer)


@pytest.fixture
def client():
    app = create_app(debug=True)
    return TestClient(app)


@pytest.fixture
def snapshots_setup(client):
    client.get("/api/test/setup")
    yield
    client.get("/api/test/teardown")
