#!/usr/bin/env python3

import sys
import logging
from flask import Flask, request, jsonify, g, render_template
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from console import Console
from appengine.db_storage import DBStorage
from basemodel import Base
from app.api.api_routes import api_blueprint

# set up logging config
logging.basicConfig(level=logging.DEBUG)

# initialize Flask app and RESTful API
app = Flask(__name__)
CORS(app)

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finder.db' #address sql db storing to finder.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Database setup
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)

# Database session setup using Flask context
@app.before_request
def before_request():
    # Before each incoming request, create a new database session and assign it to 'g.session'.
    # 'g' is a special object provided by Flask for storing data during the lifetime of a request.
    # It allows sharing data between different parts of a Flask application.
    g.session = Session()

@app.teardown_request
def teardown_request(exception=None):
    # close the database session after each request
    session = g.pop('session', None)
    if session is not None:
        session.close()

if __name__ == '__main__':
    # Initialize Flask app and run it
    server_ip = '127.0.0.1'  
    log_message = f'Server is running at http://{server_ip}:5000/'
    logging.debug(log_message)
    #run flask app listen on all available public interfaces
    app.run(host='0.0.0.0', port=5000, debug=True)

