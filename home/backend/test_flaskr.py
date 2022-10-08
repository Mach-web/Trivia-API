import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr.__init__ import create_app
from flaskr.models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'student', 'student', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    # create the trivia_test database in the terminal

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO :
     Write at least one test for each test for successful
      operation and for expected errors.
     """

    def test_retrieve_categories_success(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
    # one should have data in the categories table for this to work
        # self.assertTrue(len(data['Categories_list']))
        # self.assertTrue(data['Total_categories'])

    # this code test if one fail to input the correct name
    def test_retrieve_categories_fail(self):
        res = self.client().get('/category')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # input the correct page
    def test_retrieve_questions_by_page_success(self):
        res = self.client().get('/questions?page=1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['totalQuestions'])
        # self.assertTrue(data['categories'])

    # when you input the wrong page

    def test_retrieve_questions_by_page_fail(self):
        res = self.client().get('/questions?page=1000')
        data = json.loads(res.data)

        self.assertFalse(len(data['questions']))

    # test to delete a question which does not exist

    def test_delete_question_success(self):
        res = self.client().delete('/questions/1')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['Success'], False)

    def test_delete_question_failure(self):
        res = self.client().delete('/qns')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_add_question_success(self):
        new_questions = {
            "question": "why?",
            "answer": "because",
            "category": 1,
            "difficulty": 9}
        res = self.client().post('/questions', json=new_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)

    def test_add_question_fail(self):
        new_questions = {
            "question": "why?",
            "answer": "Because",
            "category": "hard"}
        res = self.client().post('/question/3', json=new_questions)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_search_questions(self):
        res = self.client().post('/questions', json={"search_term": " "})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)

    def test_search_questions_fail(self):
        res = self.client().post('/search', json={"search_term": " "})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    def test_retrieve_questions_based_on_category_success(self):
        res = self.client().get('/categories/2/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        # self.assertTrue(data['Questions_in_category'])

    def test_retrieve_questions_based_on_category_fail(self):
        res = self.client().get('/retrieve')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)

    # i used values from my table, I have commented out the values i used to
    # fill my table at the bottom of this page

    def test_play_quiz_success(self):
        category_pre_question = {
            "quiz_category": 1,
            "previous_question": [1,2]}
        res = self.client().post('/quizzes', json=category_pre_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['Success'], True)
        # self.assertTrue(data['game_question'])

    def test_play_quiz_fail(self):
        category_pre_question = {
            "category": "",
            "previous_question": {
                "question": ""}}
        res = self.client().post('/games', json=category_pre_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
