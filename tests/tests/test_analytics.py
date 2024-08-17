import unittest
import json
from datetime import datetime
from src.app import app, db, User, ActivityLog
from flask_jwt_extended import create_access_token

class TestAnalytics(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db.create_all()

    def tearDown(self):
        db.drop_all()

    def test_log_activity(self):
        # Register and log in a user
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'password',
            'email': 'testuser@example.com'
        })
        access_token = create_access_token(identity='testuser')

        # Log activity
        response = self.app.post('/log_activity', json={
            'action': 'Watched a video'
        }, headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 201)

    def test_get_analytics(self):
        # Register and log in a user
        self.app.post('/register', json={
            'username': 'testuser',
            'password': 'password',
            'email': 'testuser@example.com'
        })
        access_token = create_access_token(identity='testuser')

        # Log some activities
        self.app.post('/log_activity', json={'action': 'Watched a video'}, headers={'Authorization': f'Bearer {access_token}'})
        self.app.post('/log_activity', json={'action': 'Liked a video'}, headers={'Authorization': f'Bearer {access_token}'})

        # Get analytics
        response = self.app.get('/analytics', headers={'Authorization': f'Bearer {access_token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json['analytics']), 2)

if __name__ == '__main__':
    unittest.main()
