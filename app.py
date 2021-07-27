import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

def create_app():
  # create and configure the app
  from .models import db, migrate
  from .config import CastingAgencyConfig


  app = Flask(__name__)
  app.config.from_object(CastingAgencyConfig)


  db.init_app(app)
  migrate.init_app(app, db)

  CORS(app)

  return app