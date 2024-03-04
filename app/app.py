#!/usr/bin/env python3

import os
import sys
import logging
import traceback
from flask import Flask, request, jsonify, g, render_template, send_from_directory, redirect
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .console import Console
from .appengine.db_storage import DBStorage
from .models.basemodel import Base
from .models.employees import employeemodel
from werkzeug.utils import secure_filename


# set up logging config
logging.basicConfig(level=logging.DEBUG)

# initialize Flask app and RESTful API
app = Flask(__name__)
CORS(app)

# Configure Flask app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/app.db' #address sql db storing to app.db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define the upload folder and allowed extensions for file uploads
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

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

#define auth file ext for uploading images
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

#check extension if is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#defining necessary routes 
# main page route 'GET'
@app.route('/')
def index():
    return render_template('main_page.html')

# create_employee route 'GET'
@app.route('/create_employee')
def create_employee():
    return render_template('create_employee.html')


# Route to handle uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# route create_employee  'POST'
@app.route('/create_employee', methods=['POST'])
def create_employee_post():
    # form sends following data 
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    employee_skills = request.form.get('employee_skills')
    education = request.form.get('education')
    employee_contact = request.form.get('employee_contact')

    try:
         # Check if a file is included in the request
        if 'photo' in request.files:
            photo = request.files['photo']

            # Check if the file is allowed and has a filename
            if photo and allowed_file(photo.filename):
                # Save the file to the UPLOAD_FOLDER
                photo_filename = secure_filename(photo.filename)
                photo.save(os.path.join(app.config['UPLOAD_FOLDER'], photo_filename))
            else:
                # Handle invalid file or filename
                return jsonify({'error': 'Invalid file or filename'}), 400
        else:
            # No photo provided, set photo_filename to None
            photo_filename = None
        
        # Create a new employeemodel instance and add it to the session
        new_employee = employeemodel(
            first_name=first_name,
            last_name=last_name, 
            employee_skills=employee_skills, 
            education=education, 
            employee_contact=employee_contact,
            photo_filename=photo_filename 
        )
        g.session.add(new_employee)
        g.session.commit()

        #construct the new employee
        new_employee_id = new_employee.id  # 'id' is the primary key of  employeemodel

        # Construct the URL dynamically
        employee_url = f'/employee/{new_employee_id}'

        #redirect to the created employee profile
        return redirect(employee_url)

        #return jsonify({'message': 'Employee created successfully'}), 201
    except SQLAlchemyError as e:
        #print exeption traceback
        traceback.print_exc()
        # Handle any database errors
        g.session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        # Close the session
        g.session.close()

#route of GET e;ployee details
@app.route('/employee/<employee_id>')
def get_employee(employee_id):
    # Retrieve employee details from the database based on the employee_id
    employee_details = g.session.query(employeemodel).filter_by(id=employee_id).first()

    # Render the employee detail template
    return render_template('employee_detail.html', employee=employee_details)


if __name__ == '__main__':
    #create folder if not exist
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    # Initialize Flask app and run it
    server_ip = '127.0.0.1'  
    log_message = f'Server is running at http://{server_ip}:5000/'
    logging.debug(log_message)
    #run flask app listen on all available public interfaces
    app.run(host='0.0.0.0', port=5000, debug=True) # debug=True useful for development but should be turned off in a production environment => debug=False.

