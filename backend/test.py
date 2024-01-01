import os
import unittest
from unittest.mock import patch
import json
from app import create_app
from models import Bird, Habitat

DELETE_ID = 1

database_path = os.environ['TEST_DATABASE_URL']
if database_path.startswith('postgres://'):
    database_path = database_path.replace('postgres://', 'postgresql://', 1)


def mock_auth_decorator(f):
    def decorated_function(g):
        return g
    if callable(f):
        return decorated_function(f)
    return decorated_function


patch('app.requires_auth', mock_auth_decorator).start()


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

        self.put_bird_success = {'habitats': [1]}
        self.put_bird_422_duplicate = {'common_name': 'Budgerigar'}
        self.post_habitat_success = {
            'name': 'Europe',
            'region_id': 4,
            'habitat_bird': 1}

        self.post_search_habitat_success = {'search': 'a'}

        self.post_habitat_400_invalid_region = {
            'name': 'Europe',
            'region_id': 1000}
        self.put_habitat_success = {'region_id': 7}

        self.put_habitat_422_duplicate_habitat = {
            'name': 'Venezuela',
            'region_id': 7}

    def tearDown(self):
        '''Executed after reach test'''
        pass

    # @patch('app.requires_auth', mock_decorator).start()
    def test_paginated_birds(self):
        res = self.client().get('/birds?page=1', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total_birds'], 1)

    def test_404_beyond_paginated_birds(self):
        res = self.client().get('/birds?page=1000', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_get_specific_bird(self):
        res = self.client().get('/birds/1', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['bird'])

    def test_404_invalid_bird(self):
        res = self.client().get('/birds/100', )
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

    def test_put_bird(self):
        res = self.client().put('/birds/1',  json=self.put_bird_success)
        data = json.loads(res.data)
        total_habitats = 0
        with self.app.app_context():
            bird = Bird.query.filter(Bird.id == 1).one_or_none()
            total_habitats = len(bird.habitats)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['bird'], 1)
        self.assertEqual(total_habitats, len(
            self.put_bird_success.get('habitats')))

    def test_422_put_bird_duplicate(self):
        res = self.client().put('/birds/1',  json=self.put_bird_422_duplicate)
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
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], delete_id)
        self.assertEqual(bird, None)

    def test_paginated_habitats(self):
        res = self.client().get('/habitats?page=1', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertGreater(data['total_habitats'], 1)

    def test_404_beyond_paginated_habitats(self):
        res = self.client().get('/habitats?page=1000', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_specific_habitat(self):
        res = self.client().get('/habitats/1', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['habitat'])

    def test_404_invalid_habitat(self):
        res = self.client().get('/habitats/1000', )
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

    def test_put_habitat(self):
        res = self.client().put('/habitats/1',  json=self.put_habitat_success)
        data = json.loads(res.data)
        region = 0
        with self.app.app_context():
            habitat = Habitat.query.filter(Habitat.id == 1).one_or_none()
            region = habitat.region_id
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['habitat'], 1)
        self.assertEqual(region, 7)

    def test_422_put_habitat_duplicate(self):
        res = self.client().put('/habitats/1',  json=self.put_habitat_422_duplicate_habitat)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Habitat name already exist')

    # TODO Delete Habitats

    def test_get_regions(self):
        res = self.client().get('/regions', )
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)


# Make the tests conveniently executable
if __name__ == '__main__':
    unittest.main()
