from tests.base import BaseTestCase

import json


class TestUsersTestcase(BaseTestCase):
    """tests for authentication"""
    def test_users_registration_empty_username(self):
        response = self.app.post('/api/v1/auth/register',
        data = json.dumps(dict(username="", email="jonnybravo@gamil.com", password="12345")),
        headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn("Username is required",response_msg["message"])

    def test_users_registration_empty_password(self):  
        """tests if registartion password is empty"""
        response = self.app.post('/api/v1/auth/register', data =json.dumps(dict(username="jonnybravo", email="jonnybravo@gamil.com", password="")), headers={'content-type':"application/json"})
        response_msg = json.loads(response.data.decode())
        self.assertIn('Password is required',response_msg["message"])

    def test_users_registration_empty_email(self):
        """tests if registartion email is empty"""        
        response = self.app.post('/api/v1/auth/register', 
        data =json.dumps(dict(username="jonnybravo", email="", password="12345")), 
        headers={'content-type':"application/json"})
        print(response)
        response_msg = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 401)
        self.assertIn("Email is required",response_msg["message"])

    def test_users_registration_correct_registration(self):
        """tests  correct login registration"""
        response = self.register_user()    
        response_msg = json.loads(response.data.decode())
        self.assertIn("User successfully registered", response_msg["message"])
     
    def test_login(self):
        """returns correct login"""
        self.register_user()
        resp = self.login_user()
        data = json.loads(resp.get_data())
        self.assertIn('token', data)



    def test_login_with_a_wrong_password(self):
        """tests API if login Works With A wrong password"""
        self.register_user()
        login= self.app.post('/api/v1/auth/login',
        data=json.dumps(dict(email="jonnybravo20@yahoo.com", password="555")), 
        content_type="application/json")
        response_msg = json.loads(login.data.decode())
        self.assertIn("Password not correct", response_msg["message"])

    def test_login_with_a_wrong_email(self):
        """tests if API accepts login with a wrong email"""
        self.register_user()
        login= self.app.post('/api/v1/auth/login',
        data=json.dumps(dict(email="jonnybravo",password="123456")),content_type="application/json")
        response_msg = json.loads(login.data.decode())
        self.assertIn("Email is invalid", response_msg["message"])



