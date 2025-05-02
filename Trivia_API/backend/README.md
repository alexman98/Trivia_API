# Backend - Trivia API

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Set up the Database

With Postgres running, create a `trivia` database:

```bash
createdb trivia
```

Populate the database using the `trivia.psql` file provided. From the `backend` folder in terminal run:

```bash
psql trivia < trivia.psql
```

### Run the Server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## To Do Tasks

These are the files you'd want to edit in the backend:

1. `backend/flaskr/__init__.py`
2. `backend/test_flaskr.py`

One note before you delve into your tasks: for each endpoint, you are expected to define the endpoint and response data. The frontend will be a plentiful resource because it is set up to expect certain endpoints and response data formats already. You should feel free to specify endpoints in your own way; if you do so, make sure to update the frontend or you will get some unexpected behavior.

1. Use Flask-CORS to enable cross-domain requests and set response headers.
2. Create an endpoint to handle `GET` requests for questions, including pagination (every 10 questions). This endpoint should return a list of questions, number of total questions, current category, categories.
3. Create an endpoint to handle `GET` requests for all available categories.
4. Create an endpoint to `DELETE` a question using a question `ID`.
5. Create an endpoint to `POST` a new question, which will require the question and answer text, category, and difficulty score.
6. Create a `POST` endpoint to get questions based on category.
7. Create a `POST` endpoint to get questions based on a search term. It should return any questions for whom the search term is a substring of the question.
8. Create a `POST` endpoint to get questions to play the quiz. This endpoint should take a category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
9. Create error handlers for all expected errors including 400, 404, 422, and 500.

## Documenting your Endpoints

You will need to provide detailed documentation of your API endpoints including the URL, request parameters, and the response body. Use the example below as a reference.

### Documentation Example

`GET '/api/v1.0/categories'`

- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, `categories`, that contains an object of `id: category_string` key: value pairs.

```json
{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"
}
```
`GET '/Categories'`
- Fetches a dictionary of all categories where the keys are the categoory IDs and the values are the category names.
- Request arguments: None
- Returns: JSON object with a success boolean and a categories object containing id:category_name key-values.

```json
{
  "categories":{
  "1": "Science",
  "2": "Art",
  "3": "Geography",
  "4": "History",
  "5": "Entertainment",
  "6": "Sports"}
}
```

`GET '/questions'`

- Fetches a paginated list of questions and returns the total number of questions, all categories and a null for current category
- Request Arguments: page (Integer value)
- Returns: A json containing:

*success - for identification that the request was successful
*questions- list of questions for the current page
*total_questions - total number of questions
*categories - a dictionary with with id and category
*current_category - null
```json

{
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": null,
  "questions": [
    {
      "answer": "Maya Angelou",
      "category": 4,
      "difficulty": 2,
      "id": 5,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
    } ],
  "success": true,
  "total_questions": 26
```

`DELETE '/questions/<int:question_id>'`

- Deletes a question by ID
- Request arguments- id as integer
- Returns a json saying if it was successful and the ID of the question

```json
{
  "success": true,
  "deleted": 12
}
```
`POST '/questions'`

- Creates a question in the database
- request arguments:
*Question (string) Text of the question
*answer (string) The answer of the question
*category (integer) The category to which the question belongs to
*difficulty (integer) The difficulty of the question (1-5)

```json
{
  "success": true,
  "created": 15
}
```

`POST 'questions/search'`

- Searches for question contining the given word
- Requests: SearchTerm (string) - the word used for the searching
- Returns a json, contaaining:
*success - indicating if it was successful
*questions - list of questions containing the given word
*total_questions - total number of found questions
*current_category - null

```json
{
  "success": true,
  "questions": [
    {
      "id": 3,
      "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?",
      "answer": "Maya Angelou",
      "category": 3,
      "difficulty": 2
    }
  ],
  "total_questions": 1,
  "current_category": null
}

```
`GET '/categories/<int:category_id>/questions'`

- Gets a paginated list of specific category
- Requires category_id (integer) for the wanted category
- Returns a json containing:
*success boolean indication if it was successful
*questions - list of questions for the given category
*total_question- total number of questions in the given category
*categories- Dictionaries of all categories

```json
{
  "success": true,
  "questions": [
    {
      "id": 7,
      "question": "Is this a test question?",
      "answer": "Yes",
      "category": 1,
      "difficulty": 1
    }
  ],
  "total_questions": 12,
  "categories": {
    "1": "Science",
    "2": "Art",
    "3": "Geography",
    "4": "History",
    "5": "Entertainment",
    "6": "Sports"
  },
  "current_category": 1
}
```

`POST '/quizzes'`
- returns a random question to play. Can be filtered by category
- requests:
*previous_questions - list of previous asked questions
*quiz category - dictionary with id and type 
- returns a json containing:
*success boolean for success
*question- random question not contained in the previous_questions
*quiz category- the selected categoty

```json
{
  "success": true,
  "question": {
    "id": 17,
    "question": "What is the capital of Italy?",
    "answer": "Rome",
    "category": 3,
    "difficulty": 2
  },
  "quiz_category": {
    "id": 3,
    "type": "Geography"
  }
}

```

## Testing

Write at least one test for the success and at least one error behavior of each endpoint using the unittest library.

To deploy the tests, run

```bash
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
