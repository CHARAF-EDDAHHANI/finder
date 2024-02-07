#!/usr/bin/env python3

import sys
import logging
from flask import Flask, request, jsonify, g, render_template
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
# Define a default route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        return jsonify({"message": "This is a POST request!"})

    return render_template('main_page.html')  # You can replace 'index.html' with your desired template

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

# Add a new route to fetch employees
@app.route('/get_employees', methods=['GET'])
def get_employees():
    try:
        # Fetch employee data from the database
        employees = g.session.query(Employee).all()  # Assuming you have an Employee model

        # Convert employee data to a list of dictionaries
        employee_data = [
            {
                'first_name': employee.first_name,
                'last_name': employee.last_name,
                'employee_skills': employee.employee_skills,
                'education': employee.education
            }
            for employee in employees
        ]

        # Return employee data as JSON
        return jsonify(employee_data)
    except SQLAlchemyError as e:
        # Handle database-related errors
        g.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# Add a new route to fetch jobs
@app.route('/get_jobs', methods=['GET'])
def get_jobs():
    try:
        # Fetch job data from the database
        jobs = g.session.query(Job).all()  # Assuming you have a Job model

        # Convert job data to a list of dictionaries
        job_data = [
            {
                'job_title': job.job_title,
                'location': job.location,
                'recruiter_contact': job.recruiter_contact,
                'job_description': job.job_description
            }
            for job in jobs
        ]

        # Return job data as JSON
        return jsonify(job_data)
    except SQLAlchemyError as e:
        # Handle database-related errors
        g.session.rollback()
        return jsonify({'error': 'Database error', 'details': str(e)}), 500
    except Exception as e:
        # Handle other unexpected errors
        return jsonify({'error': 'Internal server error', 'details': str(e)}), 500

# Add resources to the API
api.add_resource(CreateEmployeeResource, '/create_employee')


if __name__ == '__main__':
    # Initialize Flask app and run it
    server_ip = '34.229.68.97'  
    log_message = f'Server is running at http://{server_ip}:5000/'
    logging.debug(log_message)
    #run flask app listen on all available public interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)

