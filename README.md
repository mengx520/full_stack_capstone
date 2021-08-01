# Casting Agency 

## Project description
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. There are three roles in the company: Executive Producer, Casting Director and Casting Assistant. Roles are assigned with different authorization and permissions which include view, add, modify, and delete movies and actors.

## Project motivation
This is the Capstone project of Udacity's Full-Stack Nanodegree program. 
The project is aimed to demonstrate the skills of creating RESTful API, utilizing SQLAlchemy to conduct database queries, enabling role based authentication and role-based access control(BRAC) with Auth0 and JWT token, unit testing for Flask applications, error handling and final deployment to Heroku.

## Tech Stack(Dependencies)

### Backend Dependencies
Our tech stack will include the following:

* Python3 and Flask(https://flask.palletsprojects.com/en/2.0.x/)as our server language and server framework
* Virtualenv(https://virtualenv.pypa.io/en/latest/) as a tool to create isolated Python environments
* SQLAlchemy(https://www.sqlalchemy.org/) to be our ORM library of choice
* PostgreSQL(https://www.postgresql.org/) as our database of choice
* Flask-Migrate(https://flask-migrate.readthedocs.io/en/latest/) for creating and running schema migrations
* Auth0(https://auth0.com/) for authentication system management
* Heroku for deployment

#### Installing Dependencies for the Backend
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate

```

#### Development Setup

**1. Initialize and activate a virtualenv using:**
```
python -m virtualenv venv
source venv/bin/activate

```

**2. Install the dependencies:**
```
pip install -r requirements.txt

```

**3. Setup database**
With Postgres running, restore a database using the casting_agency.psql file provided. In terminal run:

```
createdb casting_agency
psql casting_agency < casting_agency.psql
```
Populating database schema
```
export DB_STRING=postgresql://<user>:<pass>@localhost:5432/<databasename>
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

**4. Run the development server:**
```
export DB_STRING=postgresql://<user>:<pass>@localhost:5432/<databasename>
export FLASK_APP=app
export FLASK_ENV=development # enables debug mode
flask run
```

**5. Testing**
```
createdb test_casting_agency
psql test_casting_agency < test_casting_agency.psql
```


### Frontend Dependencies
The frontend is using HTML, CSS, and Javascript with Bootstrap 3(https://getbootstrap.com/docs/3.4/customize/). All frontend dependencies are installed in static/, there is no need to install additional files locally.


## API Reference

### Project Host
    - Heroku: #TODO
    - Localhost: https://localhost:5000/

### Roles and Permissions
- Roles:
    - Casting Assistant: 
        - Can view actors and movies
    - Casting Director:
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    - Executive Producer:
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

### Endpoints
Get '/movies'
    - Fetch all the movies 
    - Roles Permission: Public to all three roles
    - Sample response: `curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/movies`
    ```
    {
    "movies": [
        {
            "genres": "Animation",
            "id": 1,
            "name": "WALL-E2",
            "release_date": "Tue, 17 Jun 2008 00:00:00 GMT"
        },
        {
            "genres": "Drama",
            "id": 11,
            "name": "Test",
            "release_date": "Tue, 17 Jun 2008 00:00:00 GMT"
        }
    ],
    "success": true
    }
    ```

