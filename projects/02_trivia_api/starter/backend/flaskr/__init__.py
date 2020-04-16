import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def paginate_questions(request, selection):
    page = request.args.get('page', 1, int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    formatted_questions = [question.format() for question in selection]
    page_questions = formatted_questions[start:end]

    return page_questions


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    '''
    cors = CORS(app, resources={r'*': {'origins': '*'}})

    '''
    Using the after_request decorator to set Access-Control-Allow
    '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PATCH, DELETE, OPTIONS')
        return response

    '''
    Endpoint to handle GET requests
    for all available categories.
    '''

    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.order_by(Category.id).all()
        formatted_categories = [category.type for category in categories]
        # category_dict = {category.id: category.type for category in categories}
        return jsonify({
            'success': True,
            'categories': formatted_categories
        })

    '''
    Endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    '''

    @app.route('/questions', methods=['GET'])
    def get_questions():
        questions = Question.query.order_by(Question.id).all()
        formatted_questions = paginate_questions(request, questions)
        if len(formatted_questions) == 0:
            abort(404)

        # fix off-by-one error
        for question in formatted_questions:
            question['category'] -= 1

        categories = Category.query.order_by(Category.id).all()
        category_list = [category.type for category in categories]
        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'categories': category_list,
            'current_category': ''
        })

    '''
    Endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        question = Question.query.get(question_id)
        if question is None:
            abort(404)
        question.delete()
        return jsonify({
            'success': True,
            'question_id': question_id
        })

    '''
    Endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    '''

    @app.route('/questions', methods=['POST'])
    def add_question():
        all_data = request.get_json()
        question_text = all_data['question']
        answer = all_data['answer']
        category = all_data['category']
        difficulty = all_data['difficulty']
        for param in [question_text, answer, category, difficulty]:
            if param is None:
                abort(400)

        try:
            question = Question(question_text, answer, category, difficulty)

        except:
            abort(400)

        try:
            question.insert()
        except:
            abort(500)

        return jsonify({
            'success': True
        })

    '''
    POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    '''

    # TODO ask whether this is the right naming convention
    #      not sure whether it should just be /questions

    @app.route('/questions_search', methods=['POST'])
    def search_questions():
        try:
            search_term = request.get_json()['searchTerm']
        except:
            abort(400)

        if search_term is None:
            abort(400)

        questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': ''
        })

    '''
    GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    '''

    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        # fix off-by-one error
        category_id += 1
        try:
            questions = Question.query.filter(Question.category == category_id).all()
            category = Category.query.get(category_id)
            if questions is None or category is None:
                abort(404)
        except:
            abort(404)

        formatted_questions = [question.format() for question in questions]

        return jsonify({
            'success': True,
            'questions': formatted_questions,
            'total_questions': len(questions),
            'current_category': category.type
        })

    '''
    POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    '''

    @app.route('/quizzes', methods=['POST'])
    def get_quiz():
        try:
            all_data = request.get_json()
            quiz_category = all_data['quiz_category']
            previous_questions = all_data['previous_questions']

            category_id = int(quiz_category['id'])

            # fix off-by-one error
            category_id += 1
        except:
            abort(400)

        if quiz_category is None:
            abort(400)

        all_category_questions = Question.query.filter(Question.category == category_id).all()

        if len(previous_questions) == len(all_category_questions):
            return jsonify({
                'success': True,
                'question': None
            })

        if len(previous_questions) > 0:
            remaining_questions = [question for question in all_category_questions if question.id not in previous_questions]
        else:
            remaining_questions = all_category_questions

        if len(remaining_questions) == 0:
            abort(404)

        next_question = random.choice(remaining_questions)

        return jsonify({
            'success': True,
            'question': next_question.format()
        })

    '''
    Error handlers for all expected errors
    including 404 and 422.
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'bad request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'unprocessable'
        }), 422

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'server error'
        }), 500

    return app
