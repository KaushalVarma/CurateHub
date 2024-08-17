import unittest
import json
from src.app import app, db, User
from flask_jwt_extended import create_access_token

class TestUserProfile(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_register_user(self):
        response = self.app.post('/register', json={
            'username': 'testuser',
            'password': 'password',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 201)

    def test_update_profile(self):
        # Register and log in a user
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'password',
            'email': 'testuser@example.com'
        })
        access_token = create_access_token(identity='testuser')
        
        # Update profile
        response = self.app.put('/profile', json={
            'preferences': 'Python, Data Science'
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)

    def test_get_profile(self):
        # Register and log in a user
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'password',
            'email': 'testuser@example.com'
        })
        access_token = create_access_token(identity='testuser')
        
        # Get profile
        response = self.app.get('/profile', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('testuser', response.json['username'])

if __name__ == '__main__':
    unittest.main()
