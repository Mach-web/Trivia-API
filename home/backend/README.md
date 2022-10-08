## Installing dependencies

This code uses standard HTTP response codes and verbs.

You need to have the required modules installed before starting the server. You need to have already installed python and pip. 

You can use the following commands.

pip install sqlalchemy

pip install flask_sqlachemy

pip install  flask

pip install  flask_migrate

pip install flask_cors

## Running the server

In order to start the flask app, run the following commands in your terminal.

For windows:
       set FLASK_APP=flaskr
            
       set FLASK_ENV=development

       flask run

For MacOS:
       export FLASK_APP=flaskr
            
       export FLASK_ENV=development

       flask run

The following commands will start the API app.

In order to get started with passing instructions to the API, open another terminal tab.


## API REFERENCES


### Getting started
The backend is hosted at http://127.0.0.1:5000/ and at present can only be run locally.
The app does not require any authentication


### Error handling
Errors are quite common when running an API. In this backend app errors are handled as JSON objects in the following format:

{

'Success': False,

'Error': 404,

'Message': Not found

}

The following errors are return incase the API fails:

'400':'Bad Request',
    
'404':'Not Found',
    
'422':'Unprocessable Entity'

### ENDPOINTS

GET/categories

General:

       Returns a list of categories with details.
       
       Returns the total number of categories.
       
Sample: curl http://127.0.0.1:5000/categories

{
       'Success': True,
       'Categories_list': [{
       'id':"1",
       'type': "Science"
       },{
       'id': "2",
       'type': "Art"
       },{
       'id': "3",
       'type': "Geography"
       },{
       'id': "4",
       'type': "History"
       },{
       'id': "5",
       'type': "Entertainment"
       },{
       'id': "6",
       'type': "Sports"
       }],
       'Total_categories': 6
}



GET/questions

General:

       Returns a list of questions with details per page.
       
       Returns the total number of questions.
        
       List of categories.
    
       Current Directory.
       
Sample: curl http://127.0.0.1:5000/questions?page=1

{
       'Success': True,
       'List-of-questions': [{
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
       }],
       'Total_questions': 100,
       'Current_category': None,
       'categories': [{
       'id':"1",
       'type': "Science"
       },{
       'id': "2",
       'type': "Art"
       },{
       'id': "3",
       'type': "Geography"
       },{
       'id': "4",
       'type': "History"
       },{
       'id': "5",
       'type': "Entertainment"
       },{
       'id': "6",
       'type': "Sports"
       }]
}




DELETE/questions/{question_id}

General:

       Returns deleted question id.
       
Sample: curl http://127.0.0.1:5000/questions/1

{
       'Success': True,
       'Deleted_question_id': 1
}



POST/questions

General:

       Enables the user to create new questions.
       
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"question":"why?","answer":"Because","category":"hard","difficulty":7}'

{
       'Success': True
}




POST/questions

General:

       Returns a list of search question results from given argument.
       
Sample: curl http://127.0.0.1:5000/questions -X POST -H "Content-Type: application/json" -d '{"search_term":"question"}'

{
       'Success': True,
       'Search_results': [{
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
      }]
}




GET/questions/{cat}

General:

       Returns a list of questions from a given category.
       
       Additional information about the questions is also given.
       
Sample: curl http://127.0.0.1:5000/questions/2

{
       'Success': True,
       'Questions_in_category': [{
      "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
       }]
}


POST/game

General:

       This is a game where you are given a random question from a given category.
        
       The random question should not be a previous question.
       
Sample: curl http://127.0.0.1:5000/game -X POST -H "Content-Type: application/json" -d '{"category":"2","previous_question":"why?"}'

{
       'Success': True,
       'Question': {
       "id": 1,
      "question": "This is a question",
      "answer": "This is an answer",
      "difficulty": 5,
      "category": 2
       }
}

```python

```
