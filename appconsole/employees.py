#!/usr/bin/env python3

import uuid
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from basemodel import BaseModel
import datetime
from sqlalchemy.sql import func

class employeemodel(BaseModel):
    __tablename__ = 'employees'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    first_name = Column(String)
    last_name = Column(String)
    employee_skills = Column(String)
    education = Column(String)
    employee_contact = Column(String)

    def __init__(self, first_name, last_name, employee_skills, education, employee_contact):
        self.first_name = first_name
        self.last_name = last_name
        self.employee_skills = employee_skills
        self.education = education
        self.employee_contact = employee_contact
