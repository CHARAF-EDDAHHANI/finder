#!/usr/bin/env python3

import uuid
from sqlalchemy import Column, String, Text
from basemodel import BaseModel

class JobOpening(BaseModel):
    __tablename__ = 'job_openings'

    Job_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    Job_title = Column(String)
    Location = Column(String)
    Recruiter_contact = Column(String)
    Job_description = Column(Text)
