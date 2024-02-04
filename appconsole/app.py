#!/usr/bin/env python3

import sys
import logging
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from console import Console
from appengine.db_storage import DBStorage  # Assuming this is the correct import path
from basemodel import Base  # Assuming this is the correct import path

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)
CORS(app)

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

# Database session setup using Flask context
@app.before_request
def before_request():
    g.session = Session()

@app.teardown_request
def teardown_request(exception=None):
    session = g.pop('session', None)
    if session is not None:
        session.close()

# Routes using Flask-RESTful
class CreateEmployeeResource(Resource):
    def post(self):
        try:
            data = request.json
            console = Console(g.session, None)
            console.create_employee(**data)
            return {"message": "Employee created successfully"}, 201
        except SQLAlchemyError as e:
            # Handle database-related errors
            g.session.rollback()  # Rollback the transaction in case of an error
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            # Handle other unexpected errors
            return {"error": "Internal server error", "details": str(e)}, 500

class CreateJobsResource(Resource):
    def post(self):
        try:
            data = request.json
            console = Console(g.session, None)
            console.create_jobs(**data)
            return {"message": "Job created successfully"}, 201
        except SQLAlchemyError as e:
            # Handle database-related errors
            g.session.rollback()  # Rollback the transaction in case of an error
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            # Handle other unexpected errors
            return {"error": "Internal server error", "details": str(e)}, 500

class SubmitFeedbackResource(Resource):
    def post(self):
        try:
            data = request.json
            console = Console(g.session, None)
            console.submit_feedback(**data)
            return {"message": "Feedback submitted successfully"}, 201
        except SQLAlchemyError as e:
            # Handle database-related errors
            g.session.rollback()  # Rollback the transaction in case of an error
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            # Handle other unexpected errors
            return {"error": "Internal server error", "details": str(e)}, 500

# Add resources to the API
api.add_resource(CreateEmployeeResource, '/create_employee')
api.add_resource(CreateJobsResource, '/create_jobs')
api.add_resource(SubmitFeedbackResource, '/submit_feedback')

if __name__ == '__main__':
    # Initialize Flask app and run it
    print("Server is running at http://127.0.0.1:5000/")
    logging.debug('Server is running at http://127.0.0.1:5000/')
    app.run(debug=True)