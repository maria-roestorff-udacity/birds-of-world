import os
import unittest
from unittest.mock import patch
import json
from app import create_app
from models import Bird, Habitat
import requests

from dotenv import load_dotenv
load_dotenv()

database_path = os.environ['TEST_DATABASE_URL']
if database_path.startswith('postgres://'):
    database_path = database_path.replace('postgres://', 'postgresql://', 1)

AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']
API_AUDIENCE = os.environ['API_AUDIENCE']

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_OWNER_USERNAME = os.getenv('AUTH0_OWNER_USERNAME')
AUTH0_OWNER_PASSWORD = os.getenv('AUTH0_OWNER_PASSWORD')
AUTH0_VIEWER_USERNAME = os.getenv('AUTH0_VIEWER_USERNAME')
AUTH0_VIEWER_PASSWORD = os.getenv('AUTH0_VIEWER_PASSWORD')

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

# print(x.json())
# owner_access_token = x.json().get('access_token', None)
# viewer_access_token = x.json().get('access_token', None)
access_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkNmLWNqNDVRSW5HOWYzVnhMUFVERCJ9.eyJpc3MiOiJodHRwczovL2Rldi11ZGFjaXR5LWZzbmQudWsuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDY1OTUyYTUzOTIzMDMyMjcyYjFiZTYyYSIsImF1ZCI6ImJpcmRzIiwiaWF0IjoxNzA0Mjg4NjUzLCJleHAiOjE3MDQzNzUwNTMsImF6cCI6ImlNNDBWM2dCbk9NS1ZBMnY0Z2FHQmxTb0xxMU50anc1IiwiZ3R5IjoicGFzc3dvcmQiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YmlyZHMiLCJwb3N0OmJpcmRzIl19.MmrDTVrdS85V5yLPnXBnMvSGzAigBZVSMoiGF7rNEF4SsW294iLEO1uN8M-PrO4XJ8Y7FqL_6cf2xiQZ-tMAtCdjaiSvHVGGXcBrjl5D3eNQK1BSQacWU4qV07RugHC_DelTUH2pyjqhiiuQVurhwkJiatImeTHAcgb6GThM9dUtWQBxJEJQOLSUcB8XvC4T2eehGEz3JXeD8lYPeB__SBS1fpB2wjuyEO32jBpEIob--qnyjFgf9oiWo5-8TqOGy5jMZnhZhI5G1STPXRE2jj2LJ3OuRMiW2-cdGI0xkGH1fG5abEGCA-vvKSYxez2wt8_E1o83dLNs9fwA8AH_rQ'

# header = {
#     'Authorization': f'Bearer {access_token}'
# }


# def mock_auth_decorator(f):
#     def decorated_function(g):
#         return g
#     if callable(f):
#         return decorated_function(f)
#     return decorated_function


# patch('app.requires_auth', mock_auth_decorator).start()


class BirdsOfTWorldsTestCase(unittest.TestCase):
    '''This class represents the birds of the world test case'''

    def setUp(self):
        '''Define test variables and initialize app.'''

        self.app = create_app(database_path)
        self.client = self.app.test_client
        self.post_bird_success = {
            'common_name': 'European Robin',
            'species': 'Erithacus_rubecula',
            'habitats': [1, 2],
            'image_link': 'https://upload.wikimedia.org/wikipedia.jpg'}
        self.post_bird_400_missing_atrribute = {
            'common_name': 'European Robin',
            'species': 'Erithacus_rubecula',
            'image_link': 'https://upload.wikimedia.org/wikipedia.jpg'}
        self.post_bird_404_habitats_not_found = {
            'common_name': 'European Robin',
            'species': 'Erithacus_rubecula',
            'habitats': [1, 2, 1000],
            'image_link': 'https://upload.wikimedia.org/wikipedia.jpg'}
        self.patch_bird_success = {'habitats': [1]}
        self.patch_bird_422_duplicate = {'common_name': 'Budgerigar'}
        self.post_habitat_success = {
            'name': 'Europe',
            'region_id': 4,
            'habitat_bird': 1}
        self.post_search_habitat_success = {'search': 'a'}
        self.post_habitat_400_invalid_region = {
            'name': 'Europe',
            'region_id': 1000}
        self.patch_habitat_success = {'region_id': 7}
        self.patch_habitat_422_duplicate_habitat = {
            'name': 'Venezuela',
            'region_id': 7}

    def tearDown(self):
        '''Executed after reach test'''
        pass

    # @patch('app.requires_auth', mock_decorator).start()
    def test_paginated_birds(self):
        res = self.client().get(
            '/birds?page=1', environ_base={'HTTP_AUTHORIZATION': f'Bearer {access_token}'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total_birds'], 1)

    def test_404_beyond_paginated_birds(self):
        res = self.client().get('/birds?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_specific_bird(self):
        res = self.client().get('/birds/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['bird'])

    def test_404_invalid_bird(self):
        res = self.client().get('/birds/100')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_bird(self):
        res = self.client().post('/birds',  json=self.post_bird_success)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['bird'], 3)

    def test_422_post_duplicate_bird(self):
        self.client().post('/birds',  json=self.post_bird_success)
        res = self.client().post('/birds',  json=self.post_bird_success)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'duplicate bird resource')

    def test_400_post_bird_missing_atrribute(self):
        res = self.client().post('/birds',  json=self.post_bird_400_missing_atrribute)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_404_post_bird_habitats_not_found(self):
        res = self.client().post('/birds',  json=self.post_bird_404_habitats_not_found)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_bird(self):
        res = self.client().patch('/birds/1',  json=self.patch_bird_success)
        data = json.loads(res.data)
        total_habitats = 0
        with self.app.app_context():
            bird = Bird.query.filter(Bird.id == 1).one_or_none()
            total_habitats = len(bird.habitats)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['bird'], 1)
        self.assertEqual(total_habitats, len(
            self.patch_bird_success.get('habitats')))

    def test_422_patch_bird_duplicate(self):
        res = self.client().patch('/birds/1',  json=self.patch_bird_422_duplicate)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bird common_name already exist')

    def test_delete_bird(self):
        delete_id = 1
        res = self.client().delete(f'/birds/{delete_id}')
        data = json.loads(res.data)
        with self.app.app_context():
            bird = Bird.query.filter(Bird.id == delete_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], delete_id)
        self.assertEqual(bird, None)

    def test__404_delete_bird(self):
        delete_id = 1000
        res = self.client().delete(f'/birds/{delete_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_paginated_habitats(self):
        res = self.client().get('/habitats?page=1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total_habitats'], 1)

    def test_404_beyond_paginated_habitats(self):
        res = self.client().get('/habitats?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_specific_habitat(self):
        res = self.client().get('/habitats/1')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['habitat'])

    def test_404_invalid_habitat(self):
        res = self.client().get('/habitats/1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_habitat(self):
        res = self.client().post('/habitats',  json=self.post_habitat_success)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['habitat'])

    def test_post_search_habitat(self):
        res = self.client().post('/habitats',  json=self.post_search_habitat_success)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['habitats'])

    def test_400_post_habitat_invalid_region(self):
        res = self.client().post('/habitats',  json=self.post_habitat_400_invalid_region)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_post_duplicate_habitat(self):
        self.client().post('/habitats',  json=self.post_habitat_success)
        res = self.client().post('/habitats',  json=self.post_habitat_success)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Habitat resource already exist')

    def test_patch_habitat(self):
        res = self.client().patch('/habitats/1',  json=self.patch_habitat_success)
        data = json.loads(res.data)
        region = 0
        with self.app.app_context():
            habitat = Habitat.query.filter(Habitat.id == 1).one_or_none()
            region = habitat.region_id
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['habitat'], 1)
        self.assertEqual(region, 7)

    def test_422_patch_habitat_duplicate(self):
        res = self.client().patch('/habitats/1',  json=self.patch_habitat_422_duplicate_habitat)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Habitat name already exist')

    def test_delete_habitat(self):
        delete_id = 1
        res = self.client().delete(f'/habitats/{delete_id}')
        data = json.loads(res.data)
        with self.app.app_context():
            habitat = Habitat.query.filter(
                Habitat.id == delete_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], delete_id)
        self.assertEqual(habitat, None)

    def test__404_delete_habitat(self):
        delete_id = 1000
        res = self.client().delete(f'/habitats/{delete_id}')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_regions(self):
        res = self.client().get('/regions', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
