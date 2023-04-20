import pytest


@pytest.fixture
def test_client():
    return TestClient(app)
