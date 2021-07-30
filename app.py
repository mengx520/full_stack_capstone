import os
from flask import Flask, json, render_template, request, abort, jsonify
from sqlalchemy.sql.operators import endswith_op
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app():
  # create and configure the app
  from .models import db, migrate, Movies, Actors
  from .config import CastingAgencyConfig


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
  # TODO ADD AUTH0

  def get_movies():
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
        raise
        return jsonify({
          'success': False,
          'message': 'Failed to create new movie'
        })



  @app.route('/actors', methods=['GET'], endpoint='actors')
  # TODO ADD AUTH0

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
        raise
        return jsonify({
          'success': False,
          'message': 'Failed to create new movie'
        })


  return app