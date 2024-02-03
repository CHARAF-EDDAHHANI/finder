#!/usr/bin/env python3

import sys
from flask import Flask, request, jsonify, g
from flask_cors import CORS
from flask_restful import Api, Resource
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from console import Console
from appengine.db_storage import DBStorage  # Assuming this is the correct import path
from basemodel import Base  # Assuming this is the correct import path


app = Flask(__name__)
api = Api(app)
CORS(app)

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finder.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
            return jsonify({"error": str(e)}), 500
        except Exception as e:
            # Handle other unexpected errors
            return jsonify({"error": str(e)}), 500

# Add resources to the API
api.add_resource(CreateEmployeeResource, '/create_employee', methods=['POST'])

if __name__ == '__main__':
    # Database setup
    engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)

    # Initialize Flask app and run it
    app.run(debug=True)
