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
export FLASK_APP=casting_agency.app
flask db init
flask db migrate -m "Initial migration."
flask db upgrade
```

**4. Run the development server:**
```
export DB_STRING=postgresql://<user>:<pass>@localhost:5432/<databasename>
export FLASK_APP=casting_agency.app
export FLASK_ENV=development # enables debug mode
flask run
```

**5. Testing**
```
python -m unittest tests.test_app
```


### Frontend Dependencies
The frontend is using HTML, CSS, and Javascript with Bootstrap 3(https://getbootstrap.com/docs/3.4/customize/). All frontend dependencies are installed in static/, there is no need to install additional files locally.


## API Reference

### Project Host
- Heroku: [#TODO]
- Localhost: [https://localhost:5000/](https://localhost:5000/)

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
Get `'/movies'`
* Fetch all the movies 
* Roles Permission: Public to all three roles
* Sample response: `curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/movies`
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

GET `'/movies/id'`
* Fetch a movie by id
* Roles Permission: Public to all three roles
* Sample response: `curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5000/movies/11`
```
{
  "movie": {
    "genres": "Drama",
    "id": 11,
    "name": "Test",
    "release_date": "Tue, 17 Jun 2008 00:00:00 GMT"
  },
  "success": true
}
```

GET `'/actors'`
* Fetch all the actors 
* Roles Permission: Public to all three roles
* Sample response: `curl -H "Authorization: Bearer <Token>" http://127.0.0.1:5000/actors`
```
{
    "actors": [
        {
            "age": 73,
            "gender": "Male",
            "id": 1,
            "name": "Ben Burtt"
        },
        {
            "age": 30,
            "gender": "Female",
            "id": 3,
            "name": "Emma"
        },
        {
            "age": 20,
            "gender": "Female",
            "id": 5,
            "name": "Test"
        }
    ],
    "success": true
}
```

GET `'/actors/id'`
* Fetch an actor by id
* Roles Permission: Public to all three roles
* Sample response: `curl -H "Authorization: Bearer <TOKEN>" http://127.0.0.1:5000/actors/1`
```
{
  "actor": {
    "age": 22,
    "gender": "Male",
    "id": 1,
    "name": "Ryan"
  },
  "success": true
}
```

POST `'/movies'`
* Create a new movie using json parameter with all three required information
* Roles permission: Executive Producer
* Sample response: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"name": "Up!", "release_date": "2021-06-01", "genres": "Animation"}' http://127.0.0.1:5000/movies`
```
{
    "created": "Up!",
    "success": true,
    "total_movies": 6
}
```
POST `'/actors'`
* Create a new actor using json parameter with all three required information
* Roles permission: Casting Director, Executive Producer
* Sample response: `curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"age":18, "gender":"Female", "name":"Anna"}' http://127.0.0.1:5000/actors`
```
{
  "created": "Anna", 
  "success": true, 
  "total_actors": 7
}
```

PATCH `'/movies/<id>`
* Edit a movie using json parameter 
* Roles permission: Casting Director, Executive Producer
* Sample response: `curl -X PATCH http://127.0.0.1:5000/movies/1 -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"name": "WALLE"}'`
```
{
  "movie": [
    {
      "genres": "Animation",
      "id": 1,
      "name": "WALLE",
      "release_date": "Wed, 18 Jun 2008 00:00:00 GMT"
    }
  ],
  "success": true
}
```

PATCH `'/actors/<id>`
* Edit a actor using json parameter 
* Roles permission: Casting Director, Executive Producer
* Sample response: `curl -X PATCH http://127.0.0.1:5000/actors/1 -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -d '{"name": "Ryan", "age":22}'`
```
{
  "actor": [
    {
      "age": 22, 
      "gender": "Male", 
      "id": 1, 
      "name": "Ryan"
    }
  ], 
  "success": true
}
```

DELETE `'/movies/1`
* DELETE a movie by providing id
* Roles permission: Executive Producer
* Sample response: `curl -H "Content-Type: application/json" -H "Authorization: Bearer <TOKEN>" -X DELETE http://127.0.0.1:5000/movies/1`
```
{
  "deleted": 1,
  "success": true,
  "total_movies": 6
}
```

DELETE `'/actors/1`
* DELETE a actors by providing id
* Roles permission: Casting Director, Executive Producer
* Sample response: `curl -H "Content-Type: application/json" -H "Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkxCQmh2OTI4OEZRT0NhTmllZnRBRCJ9.eyJpc3MiOiJodHRwczovL3hpYW9oYW4udXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYxMDNhMTA1MGY4NjY0MDA2OTJiZDg5ZiIsImF1ZCI6ImNhc3RpbmdfYWdlbmN5IiwiaWF0IjoxNjI3Nzk0NDczLCJleHAiOjE2Mjc4ODA4NzMsImF6cCI6Ilk5RnF2Wkt2N1hGOEVRd05jdW53OHQxSUpJUDQ3UUQ5Iiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.y1sgmm7NZuatxlFAr6S8d_vdOjP2ohTFxaVQxrMCKg7RvZP5XlMU1veMNIUMMmUWkrZhvsvAsfihQWwCHD4zpFydyOGGXSjE7O5V1g_pABGNQxf4OHWOccTGUXzQpXvCq0YWiHuCtxKToTJRm__WKbfSdgR1btpINvLK_vgdMlY-aIGj6gJ6DYub61ZANtWRll_Pc0nE4SNuq1PiFZkcXRKDPLppurdWJIcM-jK3AC_tLl4XIztq74s8bXLIl3HhPEDhRldLf0YxUif-ozgQB7Mz6uTiIqyoSFyq5p5ksa-W4Bb7L7JzDwfBunBn72W528y_MoYjJIF8V2JnGhvw8Q" -X DELETE http://127.0.0.1:5000/actors/5`
```
{
  "deleted": 5, 
  "success": true, 
  "total_actors": 2
}
```

### Error Handling
Errors are returned in the following json format:
```
{
    "success": False,
    "error": 404,
    "message": "resource not found"
}
```
The API returns 4 types of errors:
* 400: bad request
* 404: not found
* 422: unprocessable
* 500: internal server error
