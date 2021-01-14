import json
from test_user import BaseTest, TestUser


class TestBank(BaseTest):

    def test_post_bank(self):

        TestUser.test_post_user(self)

        encoded_data = json.dumps(self.bank1_data).encode('utf-8')

        resp = self.client.post('/login', json=self.user1_credentials)
        token = resp.json['access_token']
        response = self.client.post('/bank',data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 401)

        TestUser.test_post_admin(self)

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        encoded_data = json.dumps(self.bank1_data).encode('utf-8')
        response = self.client.post('/bank', data=encoded_data,
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': f'Bearer {token}'}
                                    )
        self.assertEqual(response.status_code, 200)


    def test_get_bank(self):

        TestUser.test_post_admin(self)

        headers = self.get_auth_headers(self.admin_credentials)

        encoded_data = json.dumps(self.bank1_data).encode('utf-8')

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        self.client.post('/bank',data=encoded_data,
            headers={'Content-Type': 'application/json',
                     'Accept': 'application/json',
                     'Authorization': f'Bearer {token}'}
        )

        resp = self.client.get('/bank/1', headers=headers)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/bank/2', headers=headers)
        self.assertEqual(resp.status_code, 400)



