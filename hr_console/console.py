#!/usr/bin/python3

import cmd
import shlex
import hr_console
import hr_console.engine
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hr_console.employee import Employee
from hr_console.jobopening import JobOpening
from hr_console.company import Company
from hr_console.engine.filestorage import FileStorage
import basemodel

DATABASE_URL = 'sqlite:///example.db'
engine = create_engine(DATABASE_URL, echo=True)
basemodel.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()


class Console(cmd.Cmd):
    intro = "Welcome to the HR Console. Type 'help' to list available commands."
    prompt = "(HR Console) "

    def __init__(self, session):
        super(Console, self).__init__()
        self.session = session

    def create_employee(self, first_name, last_name, employee_skills, education, cv_pdf, employee_contact, password, company_id=None):
        employee = Employee(first_name=first_name, last_name=last_name, employee_skills=employee_skills,
                            education=education, cv_pdf=cv_pdf, employee_contact=employee_contact,
                            password=password, company_id=company_id)
        self.session.add(employee)
        self.session.commit()
        print("Employee created successfully.")

    def create_job_opening(self, job_title, location, recruiter_contact, job_description, position_details, required_skills, company_id=None):
        job_opening = JobOpening(job_title=job_title, location=location, recruiter_contact=recruiter_contact,
                                job_description=job_description, position_details=position_details,
                                required_skills=required_skills, company_id=company_id)
        self.session.add(job_opening)
        self.session.commit()
        print("Job Opening created successfully.")

    def create_company(self, company_name, company_description, location, recruiter_contact):
        company = Company(company_name=company_name, company_description=company_description,
                          location=location, recruiter_contact=recruiter_contact)
        self.session.add(company)
        self.session.commit()
        print("Company created successfully.")

    def save_to_json(self, class_type, filename):
        objects = self.session.query(class_type).all()
        FileStorage.save_to_json(objects, filename)

    def load_from_json(self, class_type, filename):
        objects = FileStorage.load_from_json(class_type, filename)
        for obj in objects:
            self.session.add(obj)
        self.session.commit()

    def do_create_employee(self, args):
        """
        Create a new employee.
        Usage: create_employee <first_name> <last_name> <employee_skills> <education> <cv_pdf> <employee_contact> <password> [company_id]
        """
        args_list = shlex.split(args)
        if len(args_list) < 7:
            print("Invalid number of arguments. See 'help create_employee' for usage.")
            return

        self.create_employee(*args_list)

    def do_create_job_opening(self, args):
        """
        Create a new job opening.
        Usage: create_job_opening <job_title> <location> <recruiter_contact> <job_description> <position_details> <required_skills> [company_id]
        """
        args_list = shlex.split(args)
        if len(args_list) < 6:
            print("Invalid number of arguments. See 'help create_job_opening' for usage.")
            return

        self.create_job_opening(*args_list)

    def do_create_company(self, args):
        """
        Create a new company.
        Usage: create_company <company_name> <company_description> <location> <recruiter_contact>
        """
        args_list = shlex.split(args)
        if len(args_list) != 4:
            print("Invalid number of arguments. See 'help create_company' for usage.")
            return

        self.create_company(*args_list)

    def do_save_to_json(self, args):
        """
        Save instances to JSON file.
        Usage: save_to_json <class_type> <filename>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help save_to_json' for usage.")
            return

        self.save_to_json(args_list[0], args_list[1])

    def do_load_from_json(self, args):
        """
        Load instances from JSON file.
        Usage: load_from_json <class_type> <filename>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help load_from_json' for usage.")
            return

        self.load_from_json(args_list[0], args_list[1])

    def do_show(self, args):
        """
        Show details of an entity.
        Usage: show <class_type> <entity_id>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help show' for usage.")
            return

        # Implement show logic here

    def do_update(self, args):
        """
        Update details of an entity.
        Usage: update <class_type> <entity_id> <attribute_name> <new_value>
        """
        args_list = shlex.split(args)
        if len(args_list) != 4:
            print("Invalid number of arguments. See 'help update' for usage.")
            return

        # Implement update logic here

    def do_destroy(self, args):
        """
        Destroy (delete) an entity.
        Usage: destroy <class_type> <entity_id>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help destroy' for usage.")
            return

        # Implement destroy logic here

    def do_exit(self, args):
        """
        Exit the HR Console.
        """
        print("Exiting HR Console. Goodbye!")
        return True


if __name__ == "__main__":
    console_obj = Console(session)

    while True:
        print("\n--- HR Console ---")
        print("1. Create Employee")
        print("2. Create Job Opening")
        print("3. Create Company")
        print("4. Show Details")
        print("5. Update Details")
        print("6. Delete Entity")
        print("7. Save to JSON")
        print("8. Load from JSON")
        print("9. Exit")

        choice = input("Enter your choice (1-9): ")

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

            console_obj.create_employee(first_name, last_name, employee_skills, education, cv_pdf, employee_contact, password, company_id)

        elif choice == '2':
            # Input for creating a job opening
            job_title = input("Enter Job Title: ")
            location = input("Enter Location: ")
            recruiter_contact = input("Enter Recruiter Contact: ")
            job_description = input("Enter Job Description: ")
            position_details = input("Enter Position Details: ")
            required_skills = input("Enter Required Skills: ")
            company_id = input("Enter Company ID (if applicable, else press Enter): ")

            console_obj.create_job_opening(job_title, location, recruiter_contact, job_description, position_details, required_skills, company_id)

        elif choice == '3':
            # Input for creating a company
            company_name = input("Enter Company Name: ")
            company_description = input("Enter Company Description: ")
            location = input("Enter Location: ")
            recruiter_contact = input("Enter Recruiter Contact: ")

            console_obj.create_company(company_name, company_description, location, recruiter_contact)

        elif choice == '4':
            # Input for showing details
            class_type = input("Enter Class Type (Employee/JobOpening/Company): ")
            class_id = input("Enter Class ID: ")
            console_obj.do_show(f"{class_type} {class_id}")

        elif choice == '5':
            # Input for updating details
            class_type = input("Enter Class Type (Employee/JobOpening/Company): ")
            class_id = input("Enter Entity ID: ")
            attribute_name = input("Enter Attribute Name: ")
            new_value = input("Enter New Value: ")
            console_obj.do_update(f"{class_type} {class_id} {attribute_name} {new_value}")

        elif choice == '6':
            # Input for destroying (deleting) an entity
            class_type = input("Enter Class Type (Employee/JobOpening/Company): ")
            class_id = input("Enter Entity ID: ")
            console_obj.do_destroy(f"{class_type} {class_id}")

        elif choice == '7':
            # Input for saving to JSON
            class_type = input("Enter Class Type (Employee/JobOpening/Company): ")
            filename = input("Enter Filename: ")
            console_obj.do_save_to_json(f"{class_type} {filename}")

        elif choice == '8':
            # Input for loading from JSON
            class_type = input("Enter Class Type (Employee/JobOpening/Company): ")
            filename = input("Enter Filename: ")
            console_obj.do_load_from_json(f"{class_type} {filename}")

        elif choice == '9':
            print("Exiting the HR Console. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 9.")


