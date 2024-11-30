import unittest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "hello world"}


class MyTestCase(unittest.TestCase):
    def test_hello(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"msg": "hello world"})

    def test_hello_false(self):
        response = client.get("/")
        self.assertNotEqual(response.status_code, 201)
        self.assertNotEqual(response.json(), {"msg": "hello worldx"})


if __name__ == '__main__':
    unittest.main()
