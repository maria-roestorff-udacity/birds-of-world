import os
import unittest
import json
from app import create_app
import requests

database_path = os.environ['TEST_DATABASE_URL']
if database_path.startswith('postgres://'):
    database_path = database_path.replace('postgres://', 'postgresql://', 1)

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']

AUTH0_CLIENT_ID = os.environ['AUTH0_CLIENT_ID']
AUTH0_CLIENT_SECRET = os.environ['AUTH0_CLIENT_SECRET']
AUTH0_OWNER_USERNAME = os.environ['AUTH0_OWNER_USERNAME']
AUTH0_OWNER_PASSWORD = os.environ['AUTH0_OWNER_PASSWORD']
AUTH0_VIEWER_USERNAME = os.environ['AUTH0_VIEWER_USERNAME']
AUTH0_VIEWER_PASSWORD = os.environ['AUTH0_VIEWER_PASSWORD']

owner_payload = {'client_id': f'{AUTH0_CLIENT_ID}',
                 'client_secret': f'{AUTH0_CLIENT_SECRET}',
                 'audience': f'{API_AUDIENCE}',
                 'grant_type': 'password',
                 'username': f'{AUTH0_OWNER_USERNAME}',
                 'password': f'{AUTH0_OWNER_PASSWORD}'
                 }

viewer_payload = {'client_id': f'{AUTH0_CLIENT_ID}',
                  'client_secret': f'{AUTH0_CLIENT_SECRET}',
                  'audience': f'{API_AUDIENCE}',
                  'grant_type': 'password',
                  'username': f'{AUTH0_VIEWER_USERNAME}',
                  'password': f'{AUTH0_VIEWER_PASSWORD}'
                  }

headers = {'content-type': "application/json"}

url = f'https://{AUTH0_DOMAIN}/oauth/token'

owner_role = requests.post(url, headers=headers, json=owner_payload)
viewer_role = requests.post(url, headers=headers, json=viewer_payload)

owner_access_token = owner_role.json().get('access_token', None)
viewer_access_token = viewer_role.json().get('access_token', None)

headers_owner = {'Authorization': f'Bearer {owner_access_token}'}
headers_viewers = {'HTTP_AUTHORIZATION': f'Bearer {viewer_access_token}'}

print(f'owner_access_token: {owner_access_token}')
print(f'viewer_access_token: {viewer_access_token}')

class BirdsOfTWorldsTestWithRealTokensCase(unittest.TestCase):
    '''This class represents the birds of the world test case with Real tokens'''

    def setUp(self):
        '''Define test variables and initialize app.'''

        self.app = create_app(database_path)
        self.client = self.app.test_client
        self.post_bird_success = {
            'common_name': 'European Robin',
            'species': 'Erithacus_rubecula',
            'habitats': [1, 2],
            'image_link': 'https://upload.wikimedia.org/wikipedia.jpg'}

    def tearDown(self):
        '''Executed after reach test'''
        pass

    # ----------------------------------------------------------------------------#
    # RBAC Tests
    # ----------------------------------------------------------------------------#

    def test_viewer_role_get_birds(self):
        res = self.client().get(
            '/birds?page=1', environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_RBAC_birds_invalid_token(self):
        res = self.client().get(
            '/birds?page=1', environ_base={'HTTP_AUTHORIZATION': 'Bearer eyeyeyeyey'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_owner_role_post_bird(self):
        res = self.client().post('/birds',  json=self.post_bird_success,
                                 headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_403_RBAC_post_bird(self):
        res = self.client().post('/birds',  json=self.post_bird_success,
                                 headers={'Authorization': f'Bearer {viewer_access_token}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
