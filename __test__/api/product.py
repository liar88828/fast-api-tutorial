import unittest

from fastapi.testclient import TestClient

from main import app
from schema.response import Response

client = TestClient(app)


class TestProduct(unittest.TestCase):
    shared_token: str
    shared_id: str

    @classmethod
    def setUpClass(cls):
        print('--------start------------')
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
        data = response.json()
        cls.shared_token = data["data"]
        # print(self.shared_token)
        # print(data['data'])

    @classmethod
    def tearDownClass(cls):
        print(cls.shared_token)
        print('--------end------------')

    def test_product(self):
        self.test_product_create()
        self.test_product_find_all()
        self.test_product_find_id()
        self.test_product_update_id()
        self.test_product_delete_id()

    def test_product_create(self):
        print('test find create')
        response = client.post(
            "/products",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.shared_token}"

            },
            json={
                "name": "sepatu new data",
                "description": "iki sepatu anyar",
                "price": 200.00,
                "quantity": 20
            }
        )
        assert response.status_code == 200
        data: Response = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert "message" in data
        assert "code" in data
        self.shared_id = data['data']['id']

    def test_product_find_all(self):
        print('test find all')

        response = client.get(
            "/products",
            headers={
                "Content-Type": "application/json"
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert "message" in data
        assert "code" in data

    def test_product_find_id(self):
        print('test find id')
        response = client.get(
            f"/products/{self.shared_id}",
            headers={
                "Content-Type": "application/json"
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert "message" in data
        assert "code" in data

    def test_product_update_id(self):
        print('test update id')

        response = client.put(
            f"/products/{self.shared_id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.shared_token}"

            },
            json={
                "name": "update product",
                "description": "iki sepatu anyar",
                "price": 200.00,
                "quantity": 20
            }
        )

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "data" in data
        assert "message" in data
        assert "code" in data
        # print(data)
        # assert data['data']['name'] == 'update product'

    def test_product_delete_id(self):
        response = client.delete(
            f"/products/{self.shared_id}",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.shared_token}"
            },
        )
        assert response.status_code == 200
        data = response.json()
        print(data)
        assert isinstance(data, dict)
        assert "data" in data
        assert "message" in data
        assert "code" in data


if __name__ == '__main__':
    unittest.main()
