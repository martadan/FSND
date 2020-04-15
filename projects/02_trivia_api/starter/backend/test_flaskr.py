import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        username = 'danil'
        password = 'P3jzt4B4'
        address = 'localhost:5432'
        self.database_name = "trivia_test"
        # TODO swap back
        # self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        self.database_path = f"postgres://{username}:{password}@{address}/{self.database_name}"
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    At least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories(self):
        response = self.client().get('/categories')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_get_paginated_questions(self):
        response = self.client().get('/questions', query_string=dict(page=1))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']) > 0)

    def test_get_paginated_questions_second_page(self):
        response = self.client().get('/questions', query_string=dict(page=2))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']) > 0)
        self.assertTrue(len(data['questions']) < 10)

    def test_get_paginated_questions_out_of_bounds(self):
        response = self.client().get('/questions', query_string=dict(page=1000))
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_delete_question(self):
        question_id = 2
        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)
        question = Question.query.get(question_id)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(question, None)

    def test_delete_question_fail(self):
        question_id = 1000
        response = self.client().delete(f'/questions/{question_id}')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_add_question(self):
        question = 'Should this test function succeed?'
        answer = 'Yes'
        category = 2
        difficulty = 3

        response = self.client().post('/questions', data={
            'question': question,
            'answer': answer,
            'category': category,
            'difficulty': difficulty
        })
        data = json.loads(response.data)

        matching_questions = Question.query.filter(Question.question == question, Question.answer == answer).count()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(matching_questions > 0)

    def test_add_question_missing_data(self):
        question = 'Should this second test function succeed?'
        answer = 'No'

        response = self.client().post('/questions', data={
            'question': question,
            'answer': answer
        })
        data = json.loads(response.data)

        matching_questions = Question.query.filter(Question.question == question, Question.answer == answer).count()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(matching_questions, 0)

    def test_question_search(self):
        search_term = 'taj mahal'

        response = self.client().post(
            '/questions_search',
            data=json.dumps({'searchTerm': search_term}),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'] is not None)
        self.assertTrue(data['total_questions'] > 0)

    def test_question_search_missing_term(self):
        response = self.client().post('/questions_search')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)

    def test_get_by_category(self):
        category_id = 2
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'] is not None)
        self.assertTrue(data['total_questions'] > 0)

    def test_get_by_category_out_of_bounds(self):
        category_id = 100
        response = self.client().get(f'/categories/{category_id}/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)

    def test_quiz(self):
        category_id = 4
        full_category = Category.query.get(category_id).format()
        prev_questions = Question.query.filter(Question.category == category_id).all()[0:1]
        formatted_questions = [question.format() for question in prev_questions]

        response = self.client().post(
            '/quizzes',
            data=json.dumps({
                'previous_questions': formatted_questions,
                'quiz_category': full_category
            }),
            content_type='application/json'
        )
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'] is not None)

    def test_quiz_no_parameters(self):
        response = self.client().post('/quizzes')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['success'], False)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
