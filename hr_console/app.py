from flask import Flask, request, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from console import Console
from engine.db_storage import DBStorage  # Assuming this is the correct import path
from basemodel import Base  # Assuming this is the correct import path

app = Flask(__name__)
session = None  # Initialize the session as None, will be set later

@app.route('/create_employee', methods=['POST'])
def create_employee():
    data = request.json
    console = Console(session, None)
    console.create_employee(**data)
    return jsonify({"message": "Employee created successfully"}), 201

# Add similar routes for other operations (create_job_opening, create_company, etc.)

if __name__ == '__main__':
    DATABASE_URL = 'sqlite:///finder.db'
    engine = create_engine(DATABASE_URL, echo=True)
    Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    storage = DBStorage()
    storage.reload()
    
    app.run(debug=True)
