Motivation:
  This project to show my learning journey during this nanodegree
      - Database with postgres and sqlalchemy (models.py)
      - API with Flask (app.py)
      - TDD Unittest (test_app.py)
      - Authorization & Authentification Auth0 (auth.py)
      - Deployment on Heroku



Casting Agency Specifications
Models:
      - Movies: with attributes title and release date
      - Actors: with attributes name, age and gender
Endpoints:
      - GET /actors and /movies
      - DELETE /actors/ and /movies/
      - POST /actors and /movies and
      - PATCH /actors/ and /movies/
Roles:
      Casting Assistant:
              - an view actors and movies
              - email: zezena1128@gmail.com 
              - password:Test1234
      Casting Director:
              - All permissions a Casting Assistant has
              - Add or delete an actor from the database
              - Modify actors or movies
              - email: zainabeyad.zeze@gmail.com 
              - password:Test1234
      Executive Producer:
              - All permissions a Casting Director has and
              - Add or delete a movie from the database
              - email: zalkussayer@gmail.com 
              - password:Test1234
Tests:
      - One test for success behavior of each endpoint
      - One test for error behavior of each endpoint
      - At least two tests of RBAC for each role


Getting Started:
Installing Dependencies:
      - Python 3.7
                Follow instructions to install the latest version of python for your platform in the python docs

      - Virtual Enviornment:
                We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the python docs

      - PIP Dependencies:
                Once you have your virtual environment setup and running, install dependencies by naviging to the /backend directory and running:
                         
                          pip3 install -r requirements.txt
This will install all of the required packages we selected within the requirements.txt file.
      - Key Dependencies:
                - Flask is a lightweight backend microservices framework. Flask is required to  handle requests and responses.

                - SQLAlchemy and Flask-SQLAlchemy are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in ./src/database/models.py. We recommend skimming this code first so you know how to interface with the Drink model.

                - jose JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.


Running the server:
      From within the ./capstone directory first ensure you are working using your created virtual environment.

      Each time you open a new terminal session, run:
                export FLASK_APP=app.py;

      To run the server, execute:
                flask run --reload

Setup Auth0:
      1- Create a new Auth0 Account
      2- Select a unique tenant domain
      3- Create a new, single page web application
      4- Create a new API
          * in API Settings:
                - Enable RBAC
                - Enable Add Permissions in the Access Token
      5- Create new API permissions:
          * get:movies
          * get:actors
          * post:movies
          * post:actors
          * patch:movies
          * patch:actors
          * delete:movies
          * delete:actors
      6- Create new roles for:
          * Casting Assistant
                - can get:movies, get:actors
          * Casting director
                - can get:movies, get:actors, post:actors, 
                      patch:movies, patch:actors, delete:actors
          * Executive producer
                - can get:movies, get:actors, post:movies, post:actors, 
                      patch:movies, patch:actors, delete:movies, delete:actors
      8- Test your endpoints with Postman.
          * Register 3 users - assign the Casting Assistant role to the first one, Casting Director role to the second and Executive porducer to the last one.
          * Sign into each account and make note of the JWT.
          * Import the postman collection ./Casting Agency.postman_collection.json
          * Right-clicking the collection folder for Casting Assistant and Casting Director and Executive porducer, navigate to the authorization tab, and including the JWT in the token field (you should have noted these JWTs).
          * Run the collection.
          * To get tokens use this link:
                https://zainab-eyad.us.auth0.com/authorize?audience=Agency&response_type=token&client_id=HMTWTrrqyuTuufxTQEJvinQNv13le26K&redirect_uri=http://localhost:8100/tabs/user-page
              
              - Casting Assistant:
                  - email: zezena1128@gmail.com 
                  - password:Test1234
              - Casting Director:
                  - email: zainabeyad.zeze@gmail.com 
                  - password:Test1234
              - Executive Producer:
                  - email: zalkussayer@gmail.com 
                  - password:Test1234

Testing:
      To run the tests, run
                python test_app.py

API Reference:
Getting Started
Base URL: Actually, this app can be run locally and it is hosted also as a base URL using heroku (the heroku URL is  https://whispering-dusk-13865.herokuapp.com/). The backend app is hosted at the default, http://127.0.0.1:5000/, which is set as a proxy in the frontend configuration.
Authentication: This version of the application require authentication or API keys using Auth0 (Ps: The setup is givin in setup Auth0 section)
Error Handling
Errors are returned as JSON object in the following format:

{
    "success": False,
    "error": 400,
    "message": "bad request"
}

The API will return one of the error types when requests fail:
        400: Bad Request
        404: Resource Not Found
        405: Method Not allowed
        422: Not Processable
        401: AuthError Unauthorized error
        403: AuthError Permission not found

Endpoints:
        GET '/actors'
        GET '/movies'
        POST '/actors'
        POST '/movies'
        PATCH '/actors/{actor_id}'
        PATCH '/movies/{movie_id}'
        DELETE '/actors/{actor_id}'
        DELETE '/movies/{movie_id}'

        GET /actors
          Require the get:actors permission:
              Returns a list of actors
                    return jsonify({
                      'success': True,
                      'actors': actors
                    })
        GET /movies
          Require the get:movies permission
              Returns a list of movies
                    return jsonify({
                      'success': True,
                      'movies': movies
                    })

        POST /actors
          Require the post:actors permission
              Create a new row in the actors table, Returns:
                    {
                      "actors": [
                        {
                          "age": 23,
                          "gender": "Male",
                          "id": 1,
                          "name": "Actor 1"
                        }],
                      "success": true
                    }

        POST /movies
          Require the post:movies permission
              Create a new row in the movies table, Returns:
                    {
                      "movies": [
                        {
                          "id": 1,
                          "release_date": "2021/3/4",
                          "title": "Movie 1"
                        }],
                      "success": true
                    }

        PATCH /actors/<actor_id>
          Require the 'patch:actors' permission
              Update an existing row in the actors table, Returns:
                    {
                      "actors": [
                        {
                          "age": 25,
                          "gender": "female",
                          "id": 1,
                          "name": "Updated Actor 1"
                        }],
                      "success": true
                    }

        PATCH /movies/<movie_id>
          Require the patch:movies permission
              Update an existing row in the movies table, Returns:
                    {
                      "movies": [
                        {
                          "id": 1,
                          "release_date": "Thu, 15 May 2020 03:02:13 GMT",
                          "title": "Updated Movie 1"
                        }],
                      "success": true
                    }

        DELETE /actors/<actor_id>
          Require the delete:actors permission
              Delete the corresponding row for <actor_id>, Returns:
                    return jsonify({
                      "success": True,
                      "deleted": actor_id
                    })

        DELETE /movies/<movie_id>
          Require the delete:movies permission
              Delete the corresponding row for <movie_id>, Returns:
                    return jsonify({
                      "success": True,
                      "deleted": movie_id
                    })