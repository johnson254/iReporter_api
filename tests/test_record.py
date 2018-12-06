from .base import BaseTestCase

import json


class TestIntegrations(BaseTestCase):
    """tests for record enpoints"""
    def test_register_record(self):
        """ test record successfully is registered"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        register = self.app.post('/api/v1/record', data=json.dumps(dict(recordname="BAd roads real aba", description="yoyo", category="they stole again", location="NYS")),  content_type="application/json", headers={"Authorization":"Bearer {}".format(token)})
        response_msg = json.loads(register.data.decode())
        self.assertIn("Record successfully registered", response_msg["message"])
        self.assertEqual(response_msg.status_code, 201)

    def test_returns_all_record(self):
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        register =self.app.post('/api/v1/record', 
        data=json.dumps(dict(recordname="bad roads", description="yoyo", 
        category="they stole again", location="NYS")),  content_type="application/json", 
        headers={"Authorization":"Bearer {}".format(token)})
        resp = self.app.get('/api/v1/record/')
        response_data = json.loads(resp.data.decode('utf-8'))
        registered_record = response_data[0]
        self.assertEqual(registered_record['recordname'], 'bad roads')
        self.assertEqual(response_data.status_code, 201)
        

    def test_api_can_get_record_by_id(self):
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        register =self.app.post('/api/v1/record', 
        data=json.dumps(dict(recordname="bad roads", description="yoyo", 
        category="they stole again", location="NYS")),  content_type="application/json", 
        headers={"Authorization":"Bearer {}".format(token)})
        get = self.app.get('/api/v1/record/0')
        response_data = json.loads(get.data.decode('utf-8'))
        self.assertIn('bad roads', response_data['recordname'])
        self.assertEqual(response_data.status_code, 201)

    def test_get_by_ivalid_id(self):
        """tests if the get record by invalid id"""
        self.record_registration()
        response = self.app.get('/api/v1/record/4')
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Record not found", response_msg["message"])
        self.assertEqual(response_msg.status_code, 201)

    def test_add_empty_record_name(self):
        """tests addition of a empty record name"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        response = self.app.post('/api/v1/record', 
        data =json.dumps(dict(recordname="", description="yoyo", category="they stole again", location="NYS")),
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        response_msg = json.loads(response.data.decode("UTF-8"))
        self.assertIn("Recordname is required", response_msg['message'])
        self.assertEqual(response_msg.status_code, 201)


    def test_add_empty_record_location(self):
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        response = self.app.post('/api/v1/record', 
        data =json.dumps(dict(recordname="bad roads", description="yoyo", category="laptops", location="")),
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Location is required", response_msg['message'])
        self.assertEqual(response_msg.status_code, 201)

    def test_add_empty_record_description(self):
        """tests addition of a null description"""
        self.register_user()
        login = self.login_user()
        resp = json.loads(login.data.decode("UTF-8"))
        token = resp['token']
        response = self.app.post('/api/v1/record', 
        data =json.dumps(dict(recordname="bad roads", description="", category="laptops", location="NYS")),
        headers={"Authorization":"Bearer {}".format(token)},content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Description is required",response_msg['message'])
        self.assertEqual(response_msg.status_code, 201)

    def test_update_by_id(self):
        """tests if record posted can be edited"""

        self.register_user()
        self.login_user()
        self.record_registration()
        response = self.app.put('/api/v1/record/0',
        data=json.dumps(dict(recordname="Ramtoms", description="sell iron boxes", category="electronics", location="juja")), 
        content_type="application/json")
        results = self.app.get('/api/v1/record/0')
        print('hhijjmo',results)
        self.assertIn(results.content_type, 'application/json')
        self.assertEqual(response.status_code, 201)

    def test_delete(self):
        """test API can delete record"""
        self.register_user()
        login = self.login_user()
        resp= json.loads(login.data.decode('UTF-8'))
        token = resp['token']
        new_record = self.app.post('/api/v1/record', 
        data =json.dumps(dict(recordname="bad roads", description="lala", category="laptops", location="NYS")),
        headers={"Authorization":"Bearer {}".format(token)}, content_type="application/json")
        response=self.app.delete('/api/v1/record/0', 
        headers={"Authorization":"Bearer {}".format(token)}, content_type="application/json")
        response_msg = json.loads(response.data.decode())
        self.assertIn("Record successfully deleted", response_msg["message"])
        self.assertEqual(response_msg.status_code, 201)

