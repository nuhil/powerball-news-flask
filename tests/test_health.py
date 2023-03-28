import pytest
import connexion

flask_app = connexion.App(__name__, specification_dir="../")
flask_app.add_api("swagger.yml")


@pytest.fixture
def client():
    with flask_app.app.test_client() as client:
        yield client


def test_health(client):
    response = client.get('/api/health')
    assert response.status_code == 200
