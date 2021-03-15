
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class CAPSTONTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'title': 'THE FAMILY',
            'release_date': '2022/04/23'
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
    
    def test_get_movies(self):
        response = self.client().get('/movies', headers={'Authorization': f'Bearer {os.environ['CASTING_ASSISTANT_Token']}'})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])
    
    def test_get_actors(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['actors'])
        

    def test_404_sent_requesting_beyond_valid_page(self):
        response = self.client().get('/question?page=1000', json={'category': 1})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

####################################################################################
    
    def test_post_movies(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])
        self.assertEqual(data['movie']['title'], 'THE MAZE RUNNER')
        self.assertEqual(data['movie']['release_date'], '2014.09.11')
    

    def test_post_actors(self):
        response = self.client().post(
            '/actors',
            json=self.test_actor,
            headers={'Authorization': f'Bearer {EXECUTIVE_PRODUCER}'}
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'],True)
        self.assertTrue(data['movies'])
        self.assertEqual(data['movie']['title'], 'THE MAZE RUNNER')
        self.assertEqual(data['movie']['release_date'], '2014.09.11')

    def test_post_movie_unauthorized(self):
        response = self.client().post(
            '/movies',
            json=self.test_movie,
            headers={'Authorization': f'Bearer {CASTING_DIRECTOR}'}
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(data['code'], 'unauthorized')
        self.assertEqual(data['description'], 'Permission not found.')

####################################################################################

    def test_valid_post_search_questions(self):
        response = self.client().post('/questions/search',json={'searchTerm': 'title'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
      
    def test_404_envalid_post_search_questions(self):
        response = self.client().post('/questions/search',json={'searchTerm': 'zainab'})
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 404)
        self.assertFalse(data['success'])
        self.assertEqual(data['message'], 'resource not found')

####################################################################################


    def test_delete_question(self):
        res = self.client().delete('/questions/4')
        data = json.loads(res.data)
        question = Question.query.filter(Question.id == 4).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 4)
        self.assertTrue(data['questions'])
        self.assertTrue(len(data['questions']))
        self.assertEqual(question, None)
    
    def test_404_if_question_does_not_exist(self):
        res = self.client().delete('/questions/1000')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()