import os
import unittest
import json
from dotenv import load_dotenv

from flaskr import create_app
from models import db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""

        load_dotenv()
        self.database_name = os.getenv('DATABASE_NAME')
        self.database_user = os.getenv('DATABASE_USER')
        self.database_password = os.getenv('DATABASE_PASSWORD')
        self.database_host = os.getenv('DATABASE_HOST')
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    def test_get_categories(self):
        """Test GET /categories endpoint"""
        response = self.client.get('/categories')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('categories', data)
        self.assertTrue(len(data['categories']) > 0)

    def test_get_questions(self):
        """Test GET /questions endpoint"""
        response = self.client.get('/questions?page=1')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertIn('categories', data)
        self.assertTrue(len(data['questions']) > 0)


    def test_delete_question(self):
        """Test DELETE /questions/<int:question_id> endpoint"""
        with self.app.app_context():
            question = Question(question="Test question", answer="Test answer", difficulty=1, category=1)
            question.insert()
            question_id = question.id

        response = self.client.delete(f'/questions/{question_id}')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertTrue(data['success'])
        self.assertEqual(data['deleted'], question_id)

        # Optional: confirm deletion from DB
        with self.app.app_context():
            deleted_question = Question.query.get(question_id)
            self.assertIsNone(deleted_question)

    def test_create_question(self):

        """Test POST /questions endpoint"""
        new_question = {
            'question': 'Is this a test question?',
            'answer': 'Yes',
            'difficulty': 1,
            'category': 1
        }

        response = self.client.post('/questions', json=new_question)
        data = response.get_json()

        self.assertEqual(response.status_code, 201)
        self.assertTrue(data['success'])

        # Confirm creation in DB
        with self.app.app_context():
            created_question = Question.query.filter_by(question='Is this a test question?').first()
            self.assertIsNotNone(created_question)

    def test_search_questions(self):
        """Test POST /questions/search endpoint"""
        search_term = {'searchTerm': 'test'}
        response = self.client.post('/questions/search', json=search_term)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertTrue(len(data['questions']) > 0)

    def test_get_questions_by_category(self):
        """Test GET /categories/<int:category_id>/questions endpoint"""
        response = self.client.get('/categories/1/questions')
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('questions', data)
        self.assertIn('total_questions', data)
        self.assertTrue(len(data['questions']) > 0)

    def test_quiz_questions(self):
        """Test POST /quizzes endpoint"""
        quiz_data = {
            'previous_questions': [],
            'quiz_category': {'id': 1, 'type': 'Science'}
        }
        response = self.client.post('/quizzes', json=quiz_data)
        data = response.get_json()

        self.assertEqual(response.status_code, 200)
        self.assertIn('question', data)
        self.assertIn('quiz_category', data)

    def test_404_error(self):
        """Test 404 error for non-existing endpoint"""
        response = self.client.get('/non_existing_endpoint')
        self.assertEqual(response.status_code, 404)

    def test_quiz_missing_data(self):
        """Test POST /quizzes endpoint with missing data"""
        quiz_data = {
            'previous_questions': []
        }
        response = self.client.post('/quizzes', json=quiz_data)
        self.assertEqual(response.status_code, 422)

    

      


    
        

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
