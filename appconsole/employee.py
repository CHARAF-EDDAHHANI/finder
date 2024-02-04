#!/usr/bin/env python3

import uuid
from sqlalchemy import Column, String, Text
from basemodel import BaseModel

class Employee(BaseModel):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    created_at = Column(String)  # Assuming it's a string for simplicity, you may want to use DateTime
    updated_at = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    employee_skills = Column(String)
    education = Column(String)
    employee_contact = Column(String)
    photo_path = Column(String)  # Store the path to the photo

    def __init__(self, first_name, last_name, employee_skills, education, employee_contact):
        self.id = str(uuid.uuid4())
        self.first_name = first_name
        self.last_name = last_name
        self.employee_skills = employee_skills
        self.education = education
        self.employee_contact = employee_contact
