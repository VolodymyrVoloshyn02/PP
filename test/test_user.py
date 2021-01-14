import json
import unittest
from sqlalchemy.orm import close_all_sessions
from unittest.mock import ANY
from werkzeug.security import generate_password_hash

from main import app, engine, Base, session


class BaseTest(unittest.TestCase):

    client = app.test_client()
    user1_data = {
        "login": "mylogin1",
        "password": "my password",
        "name": "myname",
        "passport": "myUKRpasport",
        "address": "Lviv",
        "email": "user@gmail.com",
        "phone_number": "88005553535",
        "status": "user"
    }
    admin_data = {
        "login": "mylogin2",
        "password": "my password",
        "name": "myname",
        "passport": "myUKRpasport",
        "address": "Lviv",
        "email": "user@gmail.com",
        "phone_number": "88005553535",
        "status": "admin"
    }

    bank1_data = {
        "all_money": 500000,
        "per_cent": 30
    }
    bank2_data = {
        "all_money": 300000,
        "per_cent": 25
    }

    credit_data = {
        "start_date": "21.01.2020",
        "end_date": "21.01.2021",
        "start_sum": 1000,
        "current_sum": 100,
        "bank_id": 1,
        "user_id": 1
    }

    transaction_data = {
        "date": "17.12.2020",
        "summ": 200
    }


    def setUp(self):

        self.client = app.test_client()
        #session.commit()
        Base.metadata.create_all(engine)


        self.user1_data_hashed = {
            **self.user1_data,
            "password": generate_password_hash(self.user1_data["password"])
        }

        self.admin_data_hashed = {
            **self.admin_data,
            "password": generate_password_hash(self.admin_data["password"])
        }

        self.user1_credentials = {
            "login": self.user1_data["login"],
            "password": self.user1_data["password"]
        }

        self.admin_credentials = {
            'login': self.admin_data['login'],
            'password': self.admin_data['password']
        }

    def tearDown(self):
        #session.commit()
        close_all_sessions()
        Base.metadata.drop_all(bind=engine)

    def get_auth_headers(self, credentials):
        resp = self.client.post('/login', json = credentials)
        token = resp.json['access_token']
        return {'Authorization': f'Bearer {token}'}


class TestUser(BaseTest):

    def test_post_user(self):
                error_response = self.client.post(
                    '/user',
                    headers={'Content-Type': 'application/json',
                             'Accept': 'application/json'
                             }
                )
                self.assertEqual(error_response.status_code, 400)

                encoded_data = json.dumps(self.user1_data).encode('utf-8')
                response = self.client.post(
                    '/user',
                    data=encoded_data,
                    headers={'Content-Type': 'application/json',
                             'Accept': 'application/json'}
                )
                second_response = self.client.post(
                    '/user',
                    data=encoded_data,
                    headers={'Content-Type': 'application/json',
                             'Accept': 'application/json'}
                )
                self.assertEqual(response.status_code, 200)
                self.assertEqual(second_response.status_code, 409)

    def test_post_admin(self):

                encoded_data = json.dumps(self.admin_data).encode('utf-8')
                response = self.client.post(
                    '/user',
                    data=encoded_data,
                    headers={'Content-Type': 'application/json',
                             'Accept': 'application/json'}
                )
                self.assertEqual(response.status_code, 200)


    def test_user_login(self):

        self.test_post_user()
        resp = self.client.post('/login', json = self.user1_credentials)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json, {'access_token': ANY})



    def test_get_user_by_id(self):

        self.test_post_admin()
        headers = self.get_auth_headers(self.admin_credentials)
        resp = self.client.get('/user/1', headers=headers)
        self.assertEqual(resp.status_code,200)

        self.test_post_user()
        headers = self.get_auth_headers(self.user1_credentials)
        resp = self.client.get('/user/2', headers=headers)
        self.assertEqual(resp.status_code, 400)

    def test_get_own_user(self):

        self.test_post_admin()
        headers = self.get_auth_headers(self.admin_credentials)
        resp = self.client.get('/user', headers=headers)
        self.assertEqual(resp.status_code, 201)


        encoded_data = json.dumps(self.user1_data).encode('utf-8')
        self.client.post('/user', data=encoded_data,
                         headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json'}
                         )

        resp = self.client.get('/user',headers={
                                                'Authorization': 'Bearer dffsd.fd.fds'})
        self.assertEqual(resp.status_code, 500)



    def test_update_user(self):
        self.test_post_user()
        data = {"name": "my_NEW_name",
                "phone_number": "2223535"
                }
        #encoded_data = json.dumps(self.admin_data).encode('utf-8')
        encoded_data = json.dumps(data).encode('utf-8')
        headers = self.get_auth_headers(self.user1_credentials)
        resp = self.client.post('/login', json=self.user1_credentials)
        token = resp.json['access_token']
        response = self.client.put(
            '/user',
            data=encoded_data,headers={'Content-Type': 'application/json',
                                       'Accept': 'application/json',
                                       'Authorization': f'Bearer {token}'}
            )


        invalid_body_response = self.client.put(
            '/user',
            data='',
            headers={'Content-Type': 'application/json',
                                       'Accept': 'application/json',
                                       'Authorization': f'Bearer {token}'}
        )
        invalid_user_response = self.client.put(
            '/user/smth',
            headers={'Content-Type': 'application/json',
                                       'Accept': 'application/json',
                                       'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(invalid_user_response.status_code, 404)
        self.assertEqual(invalid_body_response.status_code, 400)

