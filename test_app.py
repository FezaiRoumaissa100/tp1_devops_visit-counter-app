import pytest

import app as app_module


class FakeRedis:
    """Faux Redis en mémoire : permet de tester sans serveur Redis."""

    def __init__(self):
        self.store = {}

    def incr(self, key):
        self.store[key] = self.store.get(key, 0) + 1
        return self.store[key]


@pytest.fixture
def fake_redis(monkeypatch):
    fake = FakeRedis()
    monkeypatch.setattr(app_module, "r", fake)
    return fake


@pytest.fixture
def client(fake_redis):
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_index_returns_200(client):
    response = client.get("/")
    assert response.status_code == 200


def test_first_visit_counts_one(client):
    response = client.get("/")
    assert "vue 1 fois" in response.get_data(as_text=True)


def test_counter_increments(client):
    client.get("/")
    client.get("/")
    response = client.get("/")
    assert "vue 3 fois" in response.get_data(as_text=True)


def test_uses_hits_key(client, fake_redis):
    client.get("/")
    assert fake_redis.store == {"hits": 1}


def test_response_contains_container_id(client, monkeypatch):
    monkeypatch.setattr(app_module.socket, "gethostname", lambda: "abc123")
    response = client.get("/")
    assert "Je suis le conteneur abc123" in response.get_data(as_text=True)
