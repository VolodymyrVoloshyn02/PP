import json
from test_user import BaseTest, TestUser


class TestCredits(BaseTest):

    def test_post_credit(self):

        TestUser.test_post_admin(self)

        encoded_data = json.dumps(self.user1_data).encode('utf-8')
        self.client.post('/user', data=encoded_data,
                         headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json'}
                         )

        encoded_data = json.dumps(self.bank1_data).encode('utf-8')

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        self.client.post('/bank',data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        encoded_data = json.dumps(self.credit_data).encode('utf-8')

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        response = self.client.post('/user/credit', data=encoded_data,
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': f'Bearer {token}'}
                                    )
        self.assertEqual(response.status_code, 400)


        encoded_data = json.dumps(self.credit_data).encode('utf-8')

        resp = self.client.post('/login', json=self.user1_credentials)
        token = resp.json['access_token']
        response = self.client.post('/user/credit', data=encoded_data,
                         headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json',
                                  'Authorization': f'Bearer {token}'}
                         )

        self.assertEqual(response.status_code, 200)



    def test_get_credit(self):
        TestUser.test_post_admin(self)

        TestUser.test_post_user(self)



        encoded_data = json.dumps(self.bank1_data).encode('utf-8')

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        self.client.post('/bank',data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        encoded_data = json.dumps(self.credit_data).encode('utf-8')

        resp = self.client.post('/login', json=self.user1_credentials)
        token = resp.json['access_token']
        self.client.post('/user/credit', data=encoded_data,
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': f'Bearer {token}'})

        headers = self.get_auth_headers(self.admin_credentials)
        resp = self.client.get('/user/credit/1', headers=headers)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/user/credit/2', headers=headers)
        self.assertEqual(resp.status_code, 400)



    def test_update_credit(self):
        TestUser.test_post_admin(self)

        TestUser.test_post_user(self)

        encoded_data = json.dumps(self.bank1_data).encode('utf-8')

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        self.client.post('/bank', data=encoded_data,
                         headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json',
                                  'Authorization': f'Bearer {token}'}
                         )

        encoded_data = json.dumps(self.credit_data).encode('utf-8')

        resp = self.client.post('/login', json=self.user1_credentials)
        token = resp.json['access_token']
        self.client.post('/user/credit', data=encoded_data,
                         headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json',
                                  'Authorization': f'Bearer {token}'})


        data = {
                    "current_sum": 88,
                }


        encoded_data = json.dumps(data).encode('utf-8')
        headers = self.get_auth_headers(self.user1_credentials)
        resp = self.client.post('/login', json=self.user1_credentials)
        token = resp.json['access_token']
        response = self.client.put(
            '/user/credit/1',
            data=encoded_data, headers={'Content-Type': 'application/json',
                                        'Accept': 'application/json',
                                        'Authorization': f'Bearer {token}'}
        )

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        data1 = {
            "current_sum": 88,
        }
        encoded_data1 = json.dumps(data1).encode('utf-8')
        invalid_body_response = self.client.put(
            '/user/credit/1',
            data=encoded_data1,
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
        self.assertEqual(invalid_body_response.status_code, 401)



