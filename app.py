import os
from flask import Flask, json, render_template, request, abort, jsonify
from sqlalchemy.sql.operators import endswith_op
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from .auth import AuthError, requires_auth
from .models import db, migrate, Movies, Actors
from .config import CastingAgencyConfig

def create_app():
  # create and configure the app


  app = Flask(__name__)
  app.config.from_object(CastingAgencyConfig)


  db.init_app(app)
  migrate.init_app(app, db)

  '''
  Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''

  CORS(app)

  '''
  Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
      response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
      response.headers.add('Access-Control-Allow-Methods', 'GET,POST,PATCH,DELETE')
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
    except:
      return jsonify({
        'success': False,
        'message': 'An error occured'
      }), 500

  @app.route('/movies', methods=['POST'], endpoint='create_movies')
  @requires_auth('post:movies')

  def create_movie():
      body = request.get_json()
      if body == {}:
        abort(422)

      new_name = body.get('name')
      new_release_date = body.get('release_date')
      new_genres = body.get('genres')

      try:
        movie = Movies(name=new_name, release_date=new_release_date, genres=new_genres)
        movie.insert()

        return jsonify({
          'success': True,
          'created': movie.id,
          'total_movies': Movies.query.count()
        }), 200
      except:
        return jsonify({
          'success': False,
          'message': 'Failed to create new movie'
        })

  @app.route('/movies/<id>', methods=['GET','PATCH'])
  @requires_auth('patch:movies')
  def edit_movies(payload, id):
      data = request.get_json()
      movie = Movies.query.filter(Movies.id == id).one_or_none()
      # it should respond with a 404 error if <id> is not found
      if not movie:
          abort(404)
      try:
        movie.name = data['name']
        movie.release_date = data['release_date']
        movie.genres = data['genres']

        movie.update()

        return jsonify({
            'success': True,
            'movie': [movie.format()]
        }), 200

      except:
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
          abort(404)

      movie.delete()

      return jsonify({
          'success': True,
          'deleted': movie.id,
          'total_movies': Movies.query.count()
      })
    except:
      abort(422)


  @app.route('/actors', methods=['GET'], endpoint='actors')
  @requires_auth('get:actors')

  def get_actors():
    try:
      actors = Actors.query.all()
      return jsonify({
        'success': True,
        'actors': [actor.format() for actor in actors]
      }), 200
    except: 
      return jsonify({
        'success': False,
        'message': 'An error occured'
      }), 500

  @app.route('/actors', methods=['POST'], endpoint='create_actors')
  @requires_auth('post:actors')

  def create_actor():
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
          'created': actor.id,
          'total_actors': Actors.query.count()
        }), 200
      except:
        return jsonify({
          'success': False,
          'message': 'Failed to create new movie'
        })

  @app.route('/actors/<id>', methods=['GET','PATCH'])
  @requires_auth('patch:actors')
  def edit_actors(id):
      data = request.get_json()
      actor = Actors.query.filter(Actors.id == id).one_or_none()
      # it should respond with a 404 error if <id> is not found
      if not actor:
          abort(404)
      try:
        actor.name = data['name']
        actor.age = data['age']
        actor.gender = data['gender']

        actor.update()

        return jsonify({
            'success': True,
            'actor': [actor.format()]
        }), 200

      except:
        return jsonify({
            'success': False,
            'message': 'An error occured'
        }), 500

  @app.route('/actors/<id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(id):
    try:
      actor = Actors.query.filter(
          Actors.id == id).one_or_none()

      if actor is None:
          abort(404)

      actor.delete()

      return jsonify({
          'success': True,
          'deleted': actor.id,
          'total_actors': Actors.query.count()
      })
    except:
        abort(422)
  



  return app