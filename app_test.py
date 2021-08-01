import os
import datetime
import unittest
import json
import urllib.parse
import urllib.request
from unittest.mock import patch

from flask_sqlalchemy import SQLAlchemy
from flask import Flask

from app import create_app
from models import db, migrate, Movies, Actors

TEST_CONFIG = {
    'TESTING': True,
    'SQLALCHEMY_DATABASE_URI': 'sqlite://',
    'SQLALCHEMY_TRACK_MODIFICATIONS': False
}

TEST_HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer test_token'
}

ASSISTANT_PAYLOAD = {
    'permissions': [
        'get:movies',
        'get:actors'
    ]
}

DIRECTOR_PAYLOAD = {
    'permissions': [
        'get:movies',
        'patch:movies',
        'get:actors',
        'post:actors',
        'patch:actors',
        'delete:actors'
    ]
}

PRODUCER_PAYLOAD = {
    'permissions': [
        'get:movies',
        'post:movies',
        'patch:movies',
        'delete:movies',
        'get:actors',
        'post:actors',
        'patch:actors',
        'delete:actors'
    ]
}

NOPERM_PAYLOAD = {
    'permissions': []
}


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app(TEST_CONFIG)

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

        self.client = self.app.test_client()
        # binds the app to the current context
        with self.app.app_context():
            db.init_app(self.app)
            # create all tables
            db.create_all()
            # add a test movie
            test_movie = Movies(
                name='Testing',
                release_date=datetime.date.today(),
                genres='Adventure')
            test_actor = Actors(name='Testing', age=19, gender='Female')
            db.session.add(test_movie)
            db.session.add(test_actor)
            db.session.commit()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_index(self):
        res = self.client.get('/')
        self.assertIn(b'<h1>Casting Agency</h1>', res.data)

    '''Test for getting movies succeed'''
    # https://docs.python.org/3/library/unittest.mock.html#unittest.mock.patch
    @patch('auth.verify_decode_jwt', return_value=ASSISTANT_PAYLOAD)
    def test_get_movies(self, mock):
        res = self.client.get('/movies', headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(len(data['movies']), 1)

    '''test getting movies failure due to movie not found'''
    @patch('auth.verify_decode_jwt', return_value=ASSISTANT_PAYLOAD)
    def test_404_if_movie_does_not_exist(self, mock):
        res = self.client.get('/movies/1000', headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''test creating movie succeed'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_create_movie(self, mock):
        res = self.client.post(
            '/movies',
            json=self.test_movie,
            headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['total_movies'])

    '''test creating actor failed due to no permission '''
    @patch('auth.verify_decode_jwt', return_value=NOPERM_PAYLOAD)
    def test_creating_actor_failed_no_permision(self, mock):
        res = self.client.post(
            '/actors',
            json=self.test_actor,
            headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    '''test creating movie failed missing information'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_422_movie_creation_failure(self, mock):
        res = self.client.post('/movies', json={}, headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    '''test editing movies succeed'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_editing_movies(self, mock):
        res = self.client.patch(
            '/movies/1',
            json=self.edited_movie,
            headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''test editing movies failed due to no permission'''
    @patch('auth.verify_decode_jwt', return_value=ASSISTANT_PAYLOAD)
    def test_editing_movie_failed_permission_denied(self, mock):
        res = self.client.patch(
            'movies/1',
            json=self.edited_movie,
            headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)

    '''test delete movies succeed'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_delete_movies(self, mock):
        res = self.client.delete('/movies/1', headers=TEST_HEADERS)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    '''test delete movies failed movie not found'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_delete_movie_not_found(self, mock):
        res = self.client.delete('/movies/100000', headers=TEST_HEADERS)

        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''test getting actor succeed'''
    @patch('auth.verify_decode_jwt', return_value=ASSISTANT_PAYLOAD)
    def test_get_actors(self, mock):
        res = self.client.get('/actors', headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    '''test getting actor failed'''
    @patch('auth.verify_decode_jwt', return_value=ASSISTANT_PAYLOAD)
    def test_404_if_actor_does_not_exist(self, mock):
        res = self.client.get('/actors/1000', headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''test creating actors succeed'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_creating_actor(self, mock):
        res = self.client.post(
            '/actors',
            json=self.test_actor,
            headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''test creating actor failed due to missing information'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_422_actor_creation_failure(self, mock):
        res = self.client.post('/actors', json={}, headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)

    '''test editing actors succeed'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_editing_actors(self, mock):
        res = self.client.patch(
            '/actors/1',
            json=self.edited_actor,
            headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''test editing actors failed due to no permission'''
    @patch('auth.verify_decode_jwt', return_value=NOPERM_PAYLOAD)
    def test_editing_actors_failed_permission_denied(self, mock):
        res = self.client.patch('actors/1', json=self.edited_actor, headers={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    '''test delete actors succeed'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_delete_actors(self, mock):
        res = self.client.delete('/actors/1', headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    '''test delete actors failed movie not found'''
    @patch('auth.verify_decode_jwt', return_value=PRODUCER_PAYLOAD)
    def test_delete_actors_not_found(self, mock):
        res = self.client.delete('/actors/100000', headers=TEST_HEADERS)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)

    '''test delete actors failed due to invalid header'''
    @patch('auth.verify_decode_jwt', return_value=NOPERM_PAYLOAD)
    def test_delete_actors_invalid_header(self, mock):
        res = self.client.delete('/actors/1', headers={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
