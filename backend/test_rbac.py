import os
import unittest
import json
from app import create_app
from models import Bird, Habitat
from time import time
from unittest.mock import patch
from mock_rsa_keys import create_test_token, mock_get_jwks


database_path = os.environ['TEST_DATABASE_URL']
if database_path.startswith('postgres://'):
    database_path = database_path.replace('postgres://', 'postgresql://', 1)

API_AUDIENCE = os.environ['API_AUDIENCE']
ALGORITHMS = os.environ['ALGORITHMS']
AUTH0_DOMAIN = os.environ['AUTH0_DOMAIN']


token_payload = {
    'iss': f'https://{AUTH0_DOMAIN}/',
    'sub': 'auth0|TestID',
    'aud': API_AUDIENCE,
    'iat': int(time()),
    'exp': int(time() + 600),
    'azp': 'TestAzp',
    'gty': 'password',
}

owner_token_payload = {
    **token_payload,
    'permissions': [
        'delete:birds',
        'delete:habitats',
        'get:birds',
        'get:habitats',
        'get:regions',
        'patch:birds',
        'patch:habitats',
        'post:birds',
        'post:habitats'
    ]
}
viewer_token_payload = {
    **token_payload,
    'permissions': [
        'get:birds',
        'get:habitats',
        'get:regions',
    ]
}

# create tokens signed with dummy private rsa key
owner_access_token = create_test_token(
    owner_token_payload, algorithm=ALGORITHMS)
viewer_access_token = create_test_token(
    viewer_token_payload, algorithm=ALGORITHMS)

# mocks the function that gets authorization from your Auth0 account
# instead use dummy public rsa key to decode token
patch('auth.get_jwks', mock_get_jwks).start()

headers_owner = {'Authorization': f'Bearer {owner_access_token}'}
headers_viewers = {'HTTP_AUTHORIZATION': f'Bearer {viewer_access_token}'}


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
            'name': 'North Europe',
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

    # ----------------------------------------------------------------------------#
    # Bird Endpoint Tests
    # ----------------------------------------------------------------------------#

    def test_paginated_birds(self):
        res = self.client().get(
            '/birds?page=1', environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total_birds'], 1)

    def test_404_beyond_paginated_birds(self):
        res = self.client().get('/birds?page=1000', environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_specific_bird(self):
        res = self.client().get('/birds/1', environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['bird'])

    def test_404_invalid_bird(self):
        res = self.client().get('/birds/100',
                                environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_bird(self):
        res = self.client().post('/birds',  json=self.post_bird_success,
                                 headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['bird'], 13)

    def test_422_post_duplicate_bird(self):
        self.client().post('/birds',  json=self.post_bird_success, headers=headers_owner)
        res = self.client().post('/birds',  json=self.post_bird_success, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'duplicate bird resource')

    def test_400_post_bird_missing_atrribute(self):
        res = self.client().post(
            '/birds',  json=self.post_bird_400_missing_atrribute, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_404_post_bird_habitats_not_found(self):
        res = self.client().post(
            '/birds',  json=self.post_bird_404_habitats_not_found, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_patch_bird(self):
        res = self.client().patch(
            '/birds/1',  json=self.patch_bird_success, headers=headers_owner)
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
        res = self.client().patch(
            '/birds/1',  json=self.patch_bird_422_duplicate, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bird common_name already exist')

    def test_delete_bird(self):
        delete_id = 1
        res = self.client().delete(
            f'/birds/{delete_id}', headers=headers_owner)
        data = json.loads(res.data)
        with self.app.app_context():
            bird = Bird.query.filter(Bird.id == delete_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], delete_id)
        self.assertEqual(bird, None)

    def test__404_delete_bird(self):
        delete_id = 1000
        res = self.client().delete(
            f'/birds/{delete_id}', headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------------------------------------#
    # Habitat Endpoint Tests
    # ----------------------------------------------------------------------------#

    def test_paginated_habitats(self):
        res = self.client().get('/habitats?page=1',
                                environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total_habitats'], 1)

    def test_404_beyond_paginated_habitats(self):
        res = self.client().get('/habitats?page=1000',
                                environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_specific_habitat(self):
        res = self.client().get('/habitats/1',
                                environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['habitat'])

    def test_404_invalid_habitat(self):
        res = self.client().get('/habitats/1000',
                                environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_post_habitat(self):
        res = self.client().post(
            '/habitats',  json=self.post_habitat_success, headers=headers_owner)
        data = json.loads(res.data)
        print(data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['habitat'])

    def test_post_search_habitat(self):
        res = self.client().post(
            '/habitats',  json=self.post_search_habitat_success, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['habitats'])

    def test_400_post_habitat_invalid_region(self):
        res = self.client().post(
            '/habitats',  json=self.post_habitat_400_invalid_region, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    def test_422_post_duplicate_habitat(self):
        self.client().post('/habitats',  json=self.post_habitat_success, headers=headers_owner)
        res = self.client().post(
            '/habitats',  json=self.post_habitat_success, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Habitat resource already exist')

    def test_patch_habitat(self):
        res = self.client().patch(
            '/habitats/1',  json=self.patch_habitat_success, headers=headers_owner)
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
        res = self.client().patch('/habitats/1',
                                  json=self.patch_habitat_422_duplicate_habitat, headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Habitat name already exist')

    def test_delete_habitat(self):
        delete_id = 1
        res = self.client().delete(
            f'/habitats/{delete_id}', headers=headers_owner)
        data = json.loads(res.data)
        with self.app.app_context():
            habitat = Habitat.query.filter(
                Habitat.id == delete_id).one_or_none()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], delete_id)
        self.assertEqual(habitat, None)

    def test_404_delete_habitat(self):
        delete_id = 1000
        res = self.client().delete(
            f'/habitats/{delete_id}', headers=headers_owner)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # ----------------------------------------------------------------------------#
    # Region Endpoint Tests
    # ----------------------------------------------------------------------------#

    def test_get_regions(self):
        res = self.client().get(
            '/regions', environ_base=headers_viewers)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_401_RBAC_get_regions(self):
        res = self.client().get('/regions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
