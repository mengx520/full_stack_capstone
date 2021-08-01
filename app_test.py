import os
import unittest
import json
import urllib.parse
import urllib.request

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from app import create_app
from models import db, migrate, Movies, Actors
from config import CastingAgencyConfig

assistant_token = os.environ.get('ASSISTANT_TOKEN')
director_token = os.environ.get('DIRECTOR_TOKEN')
producer_token = os.environ.get('PRODUCER_TOKEN')


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "test_casting_agency"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        self.migrate.init_app(test_app, db)

        # create a test movie
        self.test_movie = {
            'name': 'This is a new test movie',
            'release_date': '2021-06-01',
            'genres': 'Drama'
        }

        self.edited_movie = {
            'name': 'Editing test',
            'genres': 'Comedy'
        }

        # create a test actor
        self.test_actor = {
            'name': 'Jay',
            'age': '40',
            'gender': 'Male'
        }

        self.edited_actor = {
            'name': 'Olivia',
            'age': '18',
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    '''Test for getting movies succeed'''

    def test_get_movies(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(assistant_token)
        }
        res = self.client().get('/movies', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    '''test getting movies failure due to movie not found'''

    def test_404_if_movie_does_not_exist(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(assistant_token)
        }
        res = self.client().get('/movies/1000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test creating movie succeed'''

    def test_create_movie(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(producer_token)
        }

        res = self.client().post('/movies', json=self.test_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    '''test creating movie failed missing information'''

    def test_422_movie_creation_failure(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(producer_token)
        }
        res = self.client().post('/movies', json={}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test editing movies succeed'''

    def test_editing_movies(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(producer_token)
        }
        res = self.client().patch('/movies/1', json=self.edited_movie, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    '''test editing movies failed due to no permission'''

    def test_editing_movie_failed_permission_denied(self):
        res = self.client().patch('movies/1', json=self.edited_movie, headers='')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test delete movies succeed'''

    def test_delete_movies(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(producer_token)
        }
        res = self.client().delete('/movies/1', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    '''test delete movies failed movie not found'''

    def test_delete_movie_not_found(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(producer_token)
        }
        res = self.client().delete('/movies/100000', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''test getting actor succeed'''

    def test_get_actors(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(director_token)
        }
        res = self.client().get('/actors', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    '''test getting actor failed'''

    def test_404_if_actor_does_not_exist(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(director_token)
        }
        res = self.client().get('/actors/1000', headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test creating actors succeed'''

    def test_creating_actor(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(director_token)
        }
        res = self.client().post('/actors', json=self.test_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['created'])
        self.assertTrue(data['total_actors'])

    '''test creating actor failed due to missing information'''

    def test_422_actor_creation_failure(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(producer_token)
        }
        res = self.client().post('/actors', json={}, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test creating actor failed due to no permission '''

    def test_creating_actor_failed_no_permision(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(assistant_token)
        }

        res = self.client().post('/actors', json=self.test_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test editing actors succeed'''

    def test_editing_actors(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(producer_token)
        }
        res = self.client().patch('/actors/1', json=self.edited_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    '''test editing actors failed due to no permission'''

    def test_editing_actors_failed_permission_denied(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(assistant_token)
        }
        res = self.client().patch('actors/1', json=self.edited_actor, headers=headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test delete actors succeed'''

    def test_delete_actors(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(director_token)
        }
        res = self.client().delete('/actors/1', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    '''test delete actors failed movie not found'''

    def test_delete_actors_not_found(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer {}'.format(director_token)
        }
        res = self.client().delete('/actors/100000', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''test delete actors failed due to invalid header'''

    def test_delete_actors_invalid_header(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': "Token {}".format(director_token)
        }
        res = self.client().delete('/actors/1', headers=headers)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
