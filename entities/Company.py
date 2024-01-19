import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from basemodel import BaseModel

class Company(BaseModel):
    __tablename__ = 'companies'

    company_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    company_name = Column(String)
    company_description = Column(Text)
    location = Column(String)
    recruiter_contact = Column(String)

    employees = relationship("Employee", back_populates="company")
    job_openings = relationship("JobOpening", back_populates="company")
