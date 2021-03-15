
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import Movies, Actors, setup_db

CASTING_ASSISTANT = os.environ["CASTING_ASSISTANT_Token"]
CASTING_DIRECTOR = os.environ["CASTING_DIRECTOR_Token"]
EXECUTIVE_PRODUCER = os.environ["EXECUTIVE_PRODUCER_Token"]




class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        
        #self.database_name = "Agency"
        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
       
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'THE FAMILY',
            'release_date': '2022/04/23'
        } 
        self.new_actor = {
            'name': 'NANA',
            'gender': 'female'
        } 
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

####################################################################################
                ############ GET Test Cases "MOVIES"############

########## Success Behavior ##########
    def test_get_all_movies(self):
        response = self.client().get('/movies', 
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
    
########## Error Behavior ##########
    def test_404_get_movie_by_id(self): #????????????
        response = self.client().get('/movies/1000',
            headers = {"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

####################################################################################
                ############ POST Test Cases "MOVIES"############

########## Success Behavior ##########
    def test_post_movie(self):
        response = self.client().post('/movies', json = self.new_movie,
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))
    
########## Error Behavior ##########
    def test_401_post_movie(self):
        response = self.client().post('/movies', json = self.new_movie,
            headers = {'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

####################################################################################
                ############ PATCH Test Cases "MOVIES"############

########## Success Behavior ##########
    def test_patch_movie(self):
        response = self.client().patch('/movies/1', json = self.new_movie,
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(len(data['movies']))

########## Error Behavior ##########
    def test_422_patch_movie(self):
        response = self.client().patch('/movies/1',json={},
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

####################################################################################
                ############ DELETE Test Cases "MOVIES"############

########## Success Behavior ##########
    def test_delete_movie(self):
        movie = Movies(title='IT', release_date='2020/4/4')
        movie.insert()

        response = self.client().delete('/movies/'+str(movie.id),
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual((data['delete']), movie.id)

########## Error Behavior ##########
    def test_401_delete_movie(self):
        response = self.client().delete('/movies/6',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

#####################################################################################
#####################################################################################
                ############ GET Test Cases "ACTORS"############

########## Success Behavior ##########
    def test_get_all_actors(self):
        response = self.client().get('/actors', 
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
    
########## Error Behavior ##########
    def test_404_get_actor_by_id(self):#????????????
        response = self.client().get('/actors/1000',
            headers = {"Authorization": f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['message'], 'resource not found')

####################################################################################
                ############ POST Test Cases "ACTORS"############

########## Success Behavior ##########
    def test_post_actor(self):
        response = self.client().post('/actors', json = self.new_actor,
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))
    
########## Error Behavior ##########
    def test_401_post_actor(self):
        response = self.client().post('/actors', json = self.new_actor,
            headers = {'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

####################################################################################
                ############ PATCH Test Cases "ACTORS"############

########## Success Behavior ##########
    def test_patch_actor(self):
        response = self.client().patch('/actors/1', json = self.new_actor,
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

########## Error Behavior ##########
    def test_422_patch_actor(self):
        response = self.client().patch('/movies/1',json={},
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

####################################################################################
                ############ DELETE Test Cases "ACTORS"############

########## Success Behavior ##########
    def test_delete_actor(self):
        actor = Actors(name='NUNU', gender='male')
        actor.insert()

        response = self.client().delete('/actors/'+str(actor.id),
            headers = {'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual((data['delete']), actor.id)

########## Error Behavior ##########
    def test_401_delete_actor(self):
        response = self.client().delete('/actors/2',
            headers={'Authorization': f'Bearer {CASTING_ASSISTANT}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()