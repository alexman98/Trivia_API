from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import random

from models import setup_db, Question, Category, db

QUESTIONS_PER_PAGE = 8

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)

    if test_config is None:
        setup_db(app)
    else:
        database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
        setup_db(app, database_path=database_path)

    CORS(app, resources={r"/*": {"origins": "*"}})
    """
    Yes@TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    
    with app.app_context():
        db.create_all()

    """
    Yes@TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):

        response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS') 
        return response

    """
    Yes@TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.route('/categories', methods=['GET'])
    def get_categories():

        try:
            categories = Category.query.all()
            formatted_categories = {category.id: category.type for category in categories}
            return jsonify({
                'success': True,
                'categories': formatted_categories
            }), 200
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)


    """
    Yes@TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application 
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route('/questions', methods=['GET'])
    
    def get_questions():
        try:

            page = request.args.get('page', 1, type=int)
            pagination = Question.query.paginate(page=page, per_page=QUESTIONS_PER_PAGE, error_out=False)
            questions=[question.format() for question in pagination.items]
            total_questions = pagination.total
            #start = (page - 1) * QUESTIONS_PER_PAGE
            #end = start + QUESTIONS_PER_PAGE


            #questions = Question.query.all()
            #formatted_questions = [question.format() for question in questions] 
            #total_questions = len(formatted_questions)

            if total_questions == 0:
                abort(404)

            categories = Category.query.all()
            formatted_categories = {category.id: category.type for category in categories}

            return jsonify({
                'success': True,
                'questions': questions,
                'total_questions': total_questions,
                'categories': formatted_categories,
                'current_category': None
            }), 200
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
    """
    Yes@TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:question_id>', methods=['DELETE'])

    def delete_question(question_id):

        try:
            question = Question.query.get(question_id)
            if question is None:
                abort(404)

            question.delete()
            return jsonify({
                'success': True,
                'deleted': question_id
            }), 200
        
        except Exception as e:
            print(e)    
            db.session.rollback()
            abort(422)

    """
    Yes@TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_or_question():
        try:
            body = request.get_json()
            question= body.get('question')
            answer= body.get('answer')
            category= body.get('category')
            difficulty= body.get('difficulty')

            new_question = Question(
                question=question,
                answer=answer,
                category=category,
                difficulty=difficulty
            )
            new_question.insert()
            return jsonify({
                'success': True,
                'created': new_question.id
            }), 201
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
    """
    Yes@TODO: ###Combined with the one above.##$
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions/search', methods=['POST'])
    def search_questions():
        try:
            body= request.get_json()
            search_term = body.get('searchTerm', None)
            if search_term is None:
                abort(422)
            questions = Question.query.filter(Question.question.ilike(f'%{search_term}%')).all()
            formatted_questions = [question.format() for question in questions]

            return jsonify({
                'success': True,
                'questions': formatted_questions,
                'total_questions': len(formatted_questions),
                'current_category': None
            }), 200 

        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)
    """
    Yes@TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:category_id>/questions', methods=['GET'])
    def get_questions_by_category(category_id):
        try:
            page = request.args.get('page', 1, type=int)
            start = (page - 1) * QUESTIONS_PER_PAGE
            end = start + QUESTIONS_PER_PAGE

            questions = Question.query.filter_by(category=category_id).all()
            formatted_questions = [question.format() for question in questions]
            total_questions = len(formatted_questions)

            if total_questions == 0:
                abort(404)

            categories = Category.query.all()
            formatted_categories = {category.id: category.type for category in categories}

            return jsonify({
                'success': True,
                'questions': formatted_questions[start:end],
                'total_questions': total_questions,
                'categories': formatted_categories,
                'current_category': category_id
            }), 200
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)

    """
    Yes@TODO:

    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def play_quiz():
        try:
            body = request.get_json()
            previous_questions = body.get('previous_questions', [])
            quiz_category = body.get('quiz_category', None)

            if quiz_category is None:
                abort(422)

            if quiz_category['id'] == 0:
                questions = Question.query.all()
            else:
                questions = Question.query.filter_by(category=quiz_category['id']).all()

            questions = [question for question in questions if question.id not in previous_questions]

            if len(questions) == 0:
                return jsonify({
                    'success': True,
                    'question': None
                }), 200

            question = random.choice(questions).format()

            return jsonify({
                'success': True,
                'question': question,
                'quiz_category': quiz_category
            }), 200
        except Exception as e:
            print(e)
            db.session.rollback()
            abort(422)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.

    """
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource not found'
        }), 404
    
    @app.errorhandler(422)
    def errorhandler(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422
    @app.errorhandler(500)

    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal server error'
        }), 500
    
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad request'
        }), 400
   

    

    return app

