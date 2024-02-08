#!/usr/bin/env python3

import uuid
from sqlalchemy import Column, String, Text
from basemodel import BaseModel

class jobmodel(BaseModel):
    __tablename__ = 'jobs'

    job_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    job_title = Column(String)
    location = Column(String)
    recruiter_contact = Column(String)
    job_description = Column(Text)
