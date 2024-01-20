from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from employee import Employee
from jobopening import JobOpening
from company import Company
from filestorage import FileStorage
import basemodel

# Replace 'sqlite:///example.db' with the URL of   database
DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(DATABASE_URL, echo=True)
basemodel.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()

class Console:
    def __init__(self, session):
        self.session = session
        
    def create_employee(self, first_name, last_name, employee_skills, education, cv_pdf, employee_contact, password, company_id=None):
        employee = Employee(first_name=first_name, last_name=last_name, employee_skills=employee_skills,
                            education=education, cv_pdf=cv_pdf, employee_contact=employee_contact,
                            password=password, company_id=company_id)
        session.add(employee)
        session.commit()
        print("Employee created successfully.")

    def create_job_opening(self, job_title, location, recruiter_contact, job_description, position_details, required_skills, company_id=None):
        job_opening = JobOpening(job_title=job_title, location=location, recruiter_contact=recruiter_contact,
                                job_description=job_description, position_details=position_details,
                                required_skills=required_skills, company_id=company_id)
        session.add(job_opening)
        session.commit()
        print("Job Opening created successfully.")

    def create_company(self, company_name, company_description, location, recruiter_contact):
        company = Company(company_name=company_name, company_description=company_description,
                          location=location, recruiter_contact=recruiter_contact)
        session.add(company)
        session.commit()
        print("Company created successfully.")
        
    def save_to_json(self, class_type, filename):
        objects = self.session.query(class_type).all()
        FileStorage.save_to_json(objects, filename)

    def load_from_json(self, class_type, filename):
        objects = FileStorage.load_from_json(class_type, filename)
        for obj in objects:
            self.session.add(obj)
        self.session.commit()
        
if __name__ == "__main__":
    console = Console()

    while True:
        print("\n--- HR Console ---")
        print("1. Create Employee")
        print("2. Create Job Opening")
        print("3. Create Company")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3/4): ")

        if choice == '1':
            # Input for creating an employee
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            employee_skills = input("Enter Employee Skills: ")
            education = input("Enter Education: ")
            cv_pdf = input("Enter CV PDF: ")
            employee_contact = input("Enter Employee Contact: ")
            password = input("Enter Password: ")
            company_id = input("Enter Company ID (if applicable, else press Enter): ")

            console.create_employee(first_name, last_name, employee_skills, education, cv_pdf, employee_contact, password, company_id)

        elif choice == '2':
            # Input for creating a job opening
            job_title = input("Enter Job Title: ")
            location = input("Enter Location: ")
            recruiter_contact = input("Enter Recruiter Contact: ")
            job_description = input("Enter Job Description: ")
            position_details = input("Enter Position Details: ")
            required_skills = input("Enter Required Skills: ")
            company_id = input("Enter Company ID (if applicable, else press Enter): ")

            console.create_job_opening(job_title, location, recruiter_contact, job_description, position_details, required_skills, company_id)

        elif choice == '3':
            # Input for creating a company
            company_name = input("Enter Company Name: ")
            company_description = input("Enter Company Description: ")
            location = input("Enter Location: ")
            recruiter_contact = input("Enter Recruiter Contact: ")

            console.create_company(company_name, company_description, location, recruiter_contact)

        elif choice == '4':
            print("Exiting the HR Console. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")

