from app.api.api import app, INCIDENTS, USERS
from app.models.records import Records
from unittest import TestCase
import json


class BaseTestCase(TestCase):
    """set app config"""
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        self.record = {
            "recordname": "bad roads", "description": "bad roads real bad ",
            "category": "interviso", "location": "Ronda"}

        self.person = {
            'username': 'johson',
            'email': 'jonny bravo20@yahoo.com',
            'password': 'jonny bravo7738'
                    }

        self.reviews = {
            'title' : 'cool',
            'description': 'bad roads real bad' 
                        }
    
    def register_user(self):
        """Record registration helper"""
        resp = self.app.post('/api/v1/auth/register',
        data =json.dumps(self.person),
        headers = {'content-type': "application/json"})
        return resp

    def login_user(self):
        """User login helper"""
        resp = self.app.post('/api/v1/auth/login', 
        data=json.dumps(self.person), 
        headers={'content-type': "application/json"})
        return resp

    def record_registration(self):
        """ Record registration helper"""
        resp=self.app.post('/api/v1/record', 
        data=json.dumps(self.record), 
        headers = {'content-type': 'application/json'})
        return resp

    def tearDown(self):
        USERS.clear()
        INCIDENTS.clear()
        Records.count = 0
