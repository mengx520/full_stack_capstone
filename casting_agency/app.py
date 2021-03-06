import os
import datetime
from flask import Flask, json, render_template, request, abort, jsonify
from sqlalchemy.sql.operators import endswith_op
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .auth import AuthError, requires_auth
from .models import db, migrate, Movies, Actors
from .config import CastingAgencyConfig


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config:
        app.config.update(test_config)
    else:
        app.config.from_object(CastingAgencyConfig)

    # this is a workaround for heroku passing the incorrect DB string
    # https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
    db_uri = app.config['SQLALCHEMY_DATABASE_URI']
    if db_uri.startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = db_uri.replace("postgres://", "postgresql://", 1)

    db.init_app(app)
    migrate.init_app(app, db)

    CORS(app)

    '''
    Use the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,POST,PATCH,DELETE')
        return response

    @app.route('/')
    def index():
        return render_template('index.html')

    '''
    implement endpoint
    '''
    @app.route('/movies', methods=['GET'], endpoint='get_movies')
    @requires_auth('get:movies')
    def get_movies(payload):
        try:
            movies = Movies.query.all()
            return jsonify({
                'success': True,
                'movies': [movie.format() for movie in movies]
            }), 200
        except BaseException:
            return jsonify({
                'success': False,
                'message': 'An error occured'
            }), 500

    @app.route('/movies/<id>', methods=['GET'])
    @requires_auth('get:movies')
    def get_movie(payload, id):
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        # it should respond with a 404 error if <id> is not found
        if not movie:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'movie': movie.format()
            }), 200

    @app.route('/movies', methods=['POST'], endpoint='create_movies')
    @requires_auth('post:movies')
    def create_movie(payload):
        body = request.get_json()
        if body == {}:
            abort(422)

        new_name = body.get('name')
        new_release_date = datetime.date.fromisoformat(
            body.get('release_date'))
        new_genres = body.get('genres')

        try:
            movie = Movies(
                name=new_name,
                release_date=new_release_date,
                genres=new_genres)
            movie.insert()

            return jsonify({
                'success': True,
                'created': movie.name,
                'total_movies': Movies.query.count()
            }), 200
        except BaseException:
            return jsonify({
                'success': False,
                'message': 'Failed to create new movie'
            })

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def edit_movies(payload, id):
        data = request.get_json()
        movie = Movies.query.filter(Movies.id == id).one_or_none()
        # it should respond with a 404 error if <id> is not found
        if not movie:
            abort(404)
        try:
            if 'name' in data:
                movie.name = data['name']
            if 'release_date' in data:
                movie.release_date = data['release_date']
            if 'genres' in data:
                movie.genres = data['genres']

            movie.update()

            return jsonify({
                'success': True,
                'movie': [movie.format()]
            }), 200

        except BaseException:
            return jsonify({
                'success': False,
                'message': 'An error occured'
            }), 500

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movies(payload, id):
        try:
            movie = Movies.query.filter(
                Movies.id == id).one_or_none()

            if movie is None:
                return jsonify({
                    'success': False,
                }), 404

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': movie.id,
                'total_movies': Movies.query.count()
            })
        except BaseException:
            abort(422)

    @app.route('/actors', methods=['GET'], endpoint='actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        try:
            actors = Actors.query.all()
            return jsonify({
                'success': True,
                'actors': [actor.format() for actor in actors]
            }), 200
        except BaseException:
            return jsonify({
                'success': False,
                'message': 'An error occured'
            }), 500

    @app.route('/actors/<id>', methods=['GET'])
    @requires_auth('get:actors')
    def get_actor(payload, id):
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        # it should respond with a 404 error if <id> is not found
        if not actor:
            abort(404)
        else:
            return jsonify({
                'success': True,
                'actor': actor.format()
            }), 200

    @app.route('/actors', methods=['POST'], endpoint='create_actors')
    @requires_auth('post:actors')
    def create_actor(payload):
        body = request.get_json()
        if body == {}:
            abort(422)

        new_name = body.get('name')
        new_age = body.get('age')
        new_gender = body.get('gender')

        try:
            actor = Actors(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            return jsonify({
                'success': True,
                'created': actor.name,
                'total_actors': Actors.query.count()
            }), 200
        except BaseException:
            return jsonify({
                'success': False,
                'message': 'Failed to create new movie'
            }), 500

    @app.route('/actors/<id>', methods=['GET', 'PATCH'])
    @requires_auth('patch:actors')
    def edit_actors(payload, id):
        data = request.get_json()
        actor = Actors.query.filter(Actors.id == id).one_or_none()
        # it should respond with a 404 error if <id> is not found
        if not actor:
            abort(404)
        try:
            if 'name' in data:
                actor.name = data['name']
            if 'age' in data:
                actor.age = data['age']
            if 'gender' in data:
                actor.gender = data['gender']

            actor.update()

            return jsonify({
                'success': True,
                'actor': [actor.format()]
            }), 200

        except BaseException:
            return jsonify({
                'success': False,
                'message': 'An error occured'
            }), 500

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, id):
        try:
            actor = Actors.query.filter(
                Actors.id == id).one_or_none()

            if actor is None:
                return jsonify({
                    'success': False
                }), 404

            actor.delete()

            return jsonify({
                'success': True,
                'deleted': id,
                'total_actors': Actors.query.count()
            }), 200
        except BaseException:
            abort(422)

    # Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
  implement error handlers using the @app.errorhandler(error) decorator
  '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": 'Unathorized'
        }), 401

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": 'Internal Server Error'
        }), 500

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": "authorization error"
        }), error.status_code

    return app