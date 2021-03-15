import os
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
from models import Movies, Actors, setup_db, db_drop_and_create_all
from sqlalchemy import exc
import json
from auth import AuthError, requires_auth



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)
  

#db_drop_and_create_all()

#----------------------------------------------------------------------------#
# ENDPOINTS.
#----------------------------------------------------------------------------#

###################### Gets endpoints ######################
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_all_movies(jwt_payload):
    try:
      movies = Movies.query.all()
      all_movies = [movie.long() for movie in movies]

      return jsonify({
        'success': True,
        'movies' : all_movies
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
      }), 404
  
#####################################################
  @app.route('/movies/<int:movie_id>', methods=['GET'])
  @requires_auth('get:movies')
  def get_movies_by_id(jwt_payload, movie_id):
    try:
      
      body = request.get_json()
      if not body:
        abort(400)

      movie = Movies.query.filter(Movies.id == movie_id).one_or_none()
          
      if movie is None:
        abort(404)

      return jsonify({

        'success': True,
        'actors' : [movie.long()]
      }), 200

    except:
      return jsonify({

        "success": False, 
        "error": 404,
        "message": "resource not found"
      }), 404

  #####################################################

  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_all_actors(jwt_payload):
    try:
      actors = Actors.query.all()
      all_actors = [actor.long() for actor in actors]
          
      return jsonify({
          'success': True,
          'actors' : all_actors
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 404,
        "message": "resource not found"
      }), 404

#####################################################  
  @app.route('/actors/<int:actor_id>', methods=['GET'])
  @requires_auth('get:actors')
  def get_actorss_by_id(jwt_payload, actor_id):
    try:
          body = request.get_json()
          if not body:
              abort(400)

          actor = Actors.query.filter(Actors.id == actor_id).one_or_none()
          
          if actor is None:
              abort(404)

          return jsonify({
              'success': True,
              'actors' : [actor.long()]
          }), 200

    except:
        return jsonify({
                "success": False, 
                "error": 404,
                "message": "resource not found"
        }), 404

#####################################################################################

###################### POST endpoints ######################
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def post_movie(jwt_payload):
    try:
      body = request.get_json()
      if not body:
        abort(400)
      
      new_title = body.get('title')
      new_release_date = body.get('release_date')
      
      movie = Movies(title = new_title, release_date = new_release_date)
      movie.insert()

      return jsonify({
        'success': True,
        'movies' : [movie.long()]
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
      }), 422


  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def post_actor(jwt_payload):
    try:
      body = request.get_json()
      if not body:
        abort(400)
      
      new_name = body.get('name')
      new_gender = body.get('gender')
      if new_name is None or new_gender is None:
        abort(400)

      actor = Actors(name = new_name, gender = new_gender)
      actor.insert()

      return jsonify({
        'success': True,
        'actors' : [actor.long()]
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
      }), 422

#####################################################################################

###################### PATCH endpoints ######################
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def patch_movie(jwt_payload, movie_id):
    try:
      body = request.get_json()
      if not body:
        abort(400)

      movie_id_to_patch = Movies.query.filter(Movies.id == movie_id).one_or_none()
      if movie_id_to_patch is None:
        abort(404)
      

      new_title = body.get('title')
      new_release_date = body.get('release_date')

      movie_id_to_patch.title = new_title
      movie_id_to_patch.release_date = new_release_date

      movie_id_to_patch.update()

      return jsonify({
        'success': True,
        'movies' : [movie_id_to_patch.long()]
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
      }), 422


  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def patch_actor(jwt_payload, actor_id):
    try:
      body = request.get_json()
      if not body:
        abort(400)

      actor_id_to_patch = Actors.query.filter(Actors.id == actor_id).one_or_none()
      if actor_id_to_patch is None:
        abort(404)
      
      new_name = body.get('name')
      new_gender = body.get('gender')

      actor_id_to_patch.name = new_name
      actor_id_to_patch.gender = new_gender
      
      actor_id_to_patch.update()

      return jsonify({
        'success': True,
        'actors' : [actor_id_to_patch.long()]
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
      }), 422

#####################################################################################

###################### DELETE endpoints ######################
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movie(jwt_payload, movie_id):
    try:
      movie_id_to_delete = Movies.query.filter(Movies.id == movie_id).one_or_none()
      if movie_id_to_delete is None:
        abort(404)

      movie_id_to_delete.delete()

      return jsonify({
        'success': True,
        'delete' : movie_id
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
      }), 422


  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actor(jwt_payload, actor_id):
    try:
      actor_id_to_delete = Actors.query.filter(Actors.id == actor_id).one_or_none()
      if actor_id_to_delete is None:
        abort(404)

      actor_id_to_delete.delete()

      return jsonify({
        'success': True,
        'delete' : actor_id
      }), 200

    except:
      return jsonify({
        "success": False, 
        "error": 422,
        "message": "unprocessable"
      }), 422

#####################################################################################

###################### ERROR HANDLING ######################
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "bad request"
      }), 400

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "resource not found"
      }), 404

  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'method not allowed'
    }), 405

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "unprocessable"
    }), 422

  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'internal error'
    }), 500

#####################################################################################

###################### ERROR HANDLING FOR AUTHERROR ######################
  @app.errorhandler(AuthError)
  def handle_auth_error(e):
    response = jsonify(e.error)
    response.status_code = e.status_code
    return response

#####################################################################################

  return app

app = create_app()

if __name__ == '__main__':
  app.run()