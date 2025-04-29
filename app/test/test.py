import unittest
from flask import Flask, jsonify, request
from flask_testing import TestCase

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    identifier = data.get('username')
    password = data.get('password')
    if identifier == 'admin' and password == 'admin123':
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401


class TestFlaskApp(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        return app

    def test_index(self):
        """Тест для эндпоинта GET /"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "Hello, World!")

    def test_login_success(self):
        """Тест для успешного входа"""
        response = self.client.post('/auth/login', json={
            "username": "admin",
            "password": "admin123"
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn("Login successful", response.json['message'])

    def test_login_failure(self):
        """Тест для неудачного входа"""
        response = self.client.post('/auth/login', json={
            "username": "wrong",
            "password": "wrong"
        })
        self.assertEqual(response.status_code, 401)
        self.assertIn("Invalid credentials", response.json['message'])

if __name__ == '__main__':
    unittest.main()
