import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from basemodel import BaseModel

class JobOpening(BaseModel):
    __tablename__ = 'job_openings'

    job_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    job_title = Column(String)
    location = Column(String)
    recruiter_contact = Column(String)
    job_description = Column(Text)
    position_details = Column(Text)
    required_skills = Column(String)
    company_id = Column(String, ForeignKey('companies.company_id'))

    company = relationship("Company", back_populates="job_openings")

