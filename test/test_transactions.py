import json
from test_user import BaseTest, TestUser


class TestTransactions(BaseTest):

    def test_post_transaction(self):
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
                                  'Authorization': f'Bearer {token}'}
                         )

        encoded_data = json.dumps(self.transaction_data).encode('utf-8')

        resp = self.client.post('/login', json=self.admin_credentials)
        token = resp.json['access_token']
        response = self.client.post('/user/credit/1/transaction', data=encoded_data,
                         headers={'Content-Type': 'application/json',
                                  'Accept': 'application/json',
                                  'Authorization': f'Bearer {token}'}
                         )
        self.assertEqual(response.status_code, 400)

        resp = self.client.post('/login', json=self.user1_credentials)
        token = resp.json['access_token']
        response = self.client.post('/user/credit/1/transaction', data=encoded_data,
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': f'Bearer {token}'}
                                    )
        self.assertEqual(response.status_code, 200)


    def test_get_transaction(self):
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

        encoded_data = json.dumps(self.transaction_data).encode('utf-8')
        response = self.client.post('/user/credit/1/transaction', data=encoded_data,
                                    headers={'Content-Type': 'application/json',
                                             'Accept': 'application/json',
                                             'Authorization': f'Bearer {token}'}
                                    )
        self.assertEqual(response.status_code, 200)
        headers = self.get_auth_headers(self.user1_credentials)
        resp = self.client.get('/user/credit/1/transaction/1', headers=headers)
        self.assertEqual(resp.status_code, 201)
        resp = self.client.get('/user/credit/1/transaction/2', headers=headers)
        self.assertEqual(resp.status_code, 400)



