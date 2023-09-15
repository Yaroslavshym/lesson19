import asyncio

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture(scope='session')
def client():
    client_ = TestClient(app)
    yield client_
    del client_


@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()
