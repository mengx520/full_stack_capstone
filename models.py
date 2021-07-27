from sqlalchemy.sql.operators import nullslast_op
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# connect to a local postgresql database
db = SQLAlchemy()
migrate = Migrate()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movies(db.Model):
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    genres = db.Column(db.String(500), nullable=False)

    # TODO relationships

class Actors(db.Model):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(500), nullable=False)
    age = db.Column(db.Integer(), nullable=False)
    gender = db.Column(db.String(120), nullable=False)

    # TODO relationships