#!/usr/bin/env python3

from flask import request
from flask_restful import Resource
from sqlalchemy.exc import SQLAlchemyError
from console import Console


class CreateEmployeeResource(Resource):
    def post(self):
        try:
            data = request.json
            console = Console(g.session, None)
            console.create_employee(**data)
            return {"message": "Employee created successfully"}, 201
        except SQLAlchemyError as e:
            g.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            return {"error": "Internal server error", "details": str(e)}, 500

class CreateJobsResource(Resource):
    def post(self):
        try:
            data = request.json
            console = Console(g.session, None)
            console.create_job(**data)
            return {"message": "Job created successfully"}, 201
        except SQLAlchemyError as e:
            g.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            return {"error": "Internal server error", "details": str(e)}, 500

class SubmitFeedbackResource(Resource):
    def post(self):
        try:
            data = request.json
            console = Console(g.session, None)
            console.submit_feedback(**data)
            return {"message": "Feedback submitted successfully"}, 201
        except SQLAlchemyError as e:
            g.session.rollback()
            return {"error": "Database error", "details": str(e)}, 500
        except Exception as e:
            return {"error": "Internal server error", "details": str(e)}, 500

# Add more resource classes as needed

# create additional resource classes for fetching employees, jobs :
# class GetEmployeesResource(Resource):
#     def get(self):
#         # Logic to fetch employees from the database and return them as JSON

# class GetJobsResource(Resource):
#     def get(self):
#         # Logic to fetch jobs from the database and return them as JSON
