import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from basemodel import BaseModel

class Employee(BaseModel):
    __tablename__ = 'employees'

    employee_id = Column(String, primary_key=True, default=str(uuid.uuid4()))
    first_name = Column(String)
    last_name = Column(String)
    employee_skills = Column(String)
    education = Column(String)
    cv_pdf = Column(String)  # Assuming this is a file path or URL
    company_id = Column(String, ForeignKey('companies.company_id'))
    employee_contact = Column(String)
    password = Column(String)

    company = relationship("Company", back_populates="employees")

