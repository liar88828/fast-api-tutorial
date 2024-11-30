import unittest

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

class TestAuth(unittest.TestCase):
# shared_resource = None

    @classmethod
    def setUpClass(cls):
        print('start')

    @classmethod
    def tearDownClass(cls):
        print('end')

    def test_auth(self):
        self.test_create_register()
        self.test_create_login()

    def test_create_register(self):
        response = client.post(
            "/auth/register",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "name": "user6",
                "email": "user6@gmail.com",
                "phone": "081234512345",
                "address": "jl. supartman",
                "password": "12345678"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert "message" in data
        assert "code" in data


    def test_create_login(self):
        response = client.post(
            "/auth/login",
            headers={
                "Content-Type": "application/json"
            },
            json={
                "email": "user6@gmail.com",
                "password": "12345678"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert "message" in data
        assert "code" in data



if __name__ == '__main__':
    unittest.main()
