#!/usr/bin/env python3

from flask import Blueprint
from flask_restful import Api
from .resources import CreateEmployeeResource, CreateJobsResource, SubmitFeedbackResource


api_blueprint = Blueprint('api', __name__)
api = Api(api_blueprint)

# Add resource classes to the API
api.add_resource(CreateEmployeeResource, '/create_employee')
api.add_resource(CreateJobsResource, '/create_job')
api.add_resource(SubmitFeedbackResource, '/submit_feedback')

# Add other routes and resources as needed

# import additional resource classes

# Import the blueprint in the app.py file
# Example: from app.api.routes import api_blueprint
