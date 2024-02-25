#!/usr/bin/env python3

import uuid
from sqlalchemy import Column, String, Text
from .basemodel import BaseModel

# Inherit from the BaseModel class
class jobmodel(BaseModel):
    # Define the table name for the job model
    __tablename__ = 'jobs'

    #define culumns for the jobs table
    job_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    job_title = Column(String)
    location = Column(String)
    recruiter_contact = Column(String)
    job_description = Column(Text)

    #constructor method to initialize the model instance
    def __init__(self, job_title, location, recruiter_contact, job_description):
        self.job_title = job_title
        self.location = location
        self.recruiter_contact = recruiter_contact
        self.job_description = job_description
        super(jobmodel, self).__init__()  # Call the superclass constructor for timestamps
