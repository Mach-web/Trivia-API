# import necessary modules
import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from flaskr.models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    '''
    @TODO: Set up CORS. Allow '*' for origins.
    Delete the sample route after completing the TODOs
    '''
    # CORS(app, resources={r"*/api/*" : {origins: '*'}})
    CORS(app)
    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization')
        response.headers.add(
            'Access-Control-Allow-Headers',
            'GET,POST,PATCH,PUT,DELETE,OPTIONS')
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories')
    def list_categories():
        list_categories = Category.query.order_by('id').all()
        categories_list = {category.id: category.type for category in list_categories}
        return jsonify({
            'Success': True,
            'categories': categories_list
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.


    TEST: At this point, when you start the application,
    you should see questions and categories generated,
    ten questions per page and pagination at the
    bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * 10
        end = start + 10
        get_questions = Question.query.order_by(Question.id).all()
        questions_list = [question.format() for question in get_questions]

        categories = Category.query.order_by(Category.id).all()
        categories_list = {category.id: category.type for category in categories}

        return jsonify({
            'Success': True,
            'questions': questions_list[start:end],
            'totalQuestions': len(questions_list),
            'categories': categories_list,
            "currentCategory": None
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.
    TEST: When you click the trash icon next to a question,
    the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            question.delete()
            return jsonify({
                'Success': True,
                'Deleted_question_id': question_id
            })
        except BaseException:
            abort(422)
            return jsonify({
                'Success': False,
                'Message': 'Unprocessable Entity'
            })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end
     of the last page of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def add_question():
        body = request.get_json()

        new_question = body.get('question', None)
        new_answer = body.get('answer', None)
        new_category = body.get('category', None)
        new_difficulty = body.get('difficulty', None)

        try:
            new_questions = Question(
                question=new_question,
                answer=new_answer,
                difficulty=new_difficulty,
                category=new_category
                )
            new_questions.insert()
            return jsonify({
                'Success': True
            })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def search_questions():
        body = get_json()
        search_term = body.get('search_term')

        try:
            search_questions = Question.query.filter(
                Question.question.ilike(f'%{search_term}%')).all()
            
            search_results = [questions.format()
                              for questions in search_questions]
            
            return jsonify({
                'Success': True,
                'searchTerm': search_results,
                'totalQuestions': len(search_questions)
            })
        except BaseException:
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:cat>/questions')
    def category_questions(cat):
        try:
            cat_questions = Question.query.filter(
                Question.category == cat).all()
            cat_question = [question.format() for question in cat_questions]

            currentCategory = Category.query.filter(
                Category.id == cat
            ).all()
            currentCategory = currentCategory.format()
            return jsonify({
                'Success': True,
                'Questions_in_category': cat_question,
                'currentCategory': currentCategory,
                'totalQuestions': len(cat_question)
            })
        except BaseException:
            abort(404)

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def game():
        body = request.get_json()
        category = body.get('quiz_category')
        previous_question = body.get('previous_question')
        try:
            # get all questions in that category
            category_questions = Question.query.filter(
                Question.category == category).all()
            category_questions = [question.format()
                                  for question in category_questions]
    # make a random choice from the category questions list
            game_question = random.choice(category_questions)

            while game_question["id"] in previous_question:
                game_question = random.choice(category_questions)
            return jsonify({
                'Success': True,
                'Question': game_question
            })
        except BaseException:
            abort(404)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def badrequest(error):
        return jsonify({
            'Success': False,
            'error': 400,
            'Message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def notfound(error):
        return jsonify({
            'Success': False,
            'error': 404,
            'Message': 'Not Found'
        }), 404

    @app.errorhandler(422)
    def unprocessableentity(error):
        return jsonify({
            'Success': False,
            'error': 422,
            'Message': 'Unprocessable Entity'
        }), 422

    return app
