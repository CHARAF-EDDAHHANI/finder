#!/usr/bin/python3

import cmd
import shlex
import json
from PIL import Image
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hr_console.employee import Employee
from hr_console.jobopening import JobOpening
from hr_console.company import Company
from feedback import Feedback
from hr_console.engine.filestorage import FileStorage
import basemodel


class Console(cmd.Cmd):
    intro = "Welcome to the HR Console. Type 'help' to list available commands."
    prompt = "(HR Console) "

    def __init__(self, session):
        super().__init__()
        self.session = session
        self.storage = storage

    def search_employees(self, attribute, value):
        """Search for employees based on a specific attribute and value."""
        query = f"SELECT * FROM employees WHERE {attribute} = :value"
        result = self.session.execute(text(query), {'value': value}).fetchall()
        return result

    def filter_employees(self, filters):
        """Filter employees based on custom filters."""
        query = "SELECT * FROM employees WHERE "
        conditions = [f"{key} = :{key}" for key in filters.keys()]
        query += " AND ".join(conditions)
        result = self.session.execute(text(query), filters).fetchall()
        return result
    
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

    def upload_profile_picture(self, employee_id, image_path):
        """Upload and update the profile picture for an employee."""
        employee = self.session.query(Employee).filter_by(id=employee_id).first()
        if not employee:
            print(f"Employee with ID {employee_id} not found.")
            return

        # Validate and resize the image if needed
        image = Image.open(image_path)
        # Add logic to validate image format, size, etc.

        # Save the profile picture
        filename = f"profile_picture_{employee_id}.png"
        image.save(filename)

        # Update the employee's profile picture attribute
        employee.profile_picture = filename
        self.session.commit()
        print("Profile picture updated successfully.")

    # New method: Preview profile picture
    def preview_profile_picture(self, employee_id):
        """Preview the profile picture of an employee."""
        employee = self.session.query(Employee).filter_by(id=employee_id).first()
        if not employee or not employee.profile_picture:
            print(f"Profile picture for Employee ID {employee_id} not found.")
            return

        # Display or open the profile picture using a suitable viewer
        # You may use an external image viewer or display it directly in the console

    # New method: Crop profile picture
    def crop_profile_picture(self, employee_id, x, y, width, height):
        """Crop the profile picture of an employee."""
        employee = self.session.query(Employee).filter_by(id=employee_id).first()
        if not employee or not employee.profile_picture:
            print(f"Profile picture for Employee ID {employee_id} not found.")
            return

        # Open the profile picture
        image_path = employee.profile_picture
        image = Image.open(image_path)

        # Crop the image
        cropped_image = image.crop((x, y, x + width, y + height))

        # Save the cropped image
        filename = f"profile_picture_cropped_{employee_id}.png"
        cropped_image.save(filename)

        # Update the employee's profile picture attribute
        employee.profile_picture = filename
        self.session.commit()
        print("Profile picture cropped and updated successfully.")


    def collect_feedback(self):
        print("\nEnter your feedback:")
        user_name = input("Your Name: ")
        email = input("Your Email: ")
        subject = input("Feedback Subject: ")
        message = input("Your Feedback: ")

        feedback = Feedback(user_name, email, subject, message)
        # Optionally, we can save the feedback to a file or database for future review.
        with open('feedback.txt', 'a') as feedback_file:
            feedback_file.write(f"Name: {feedback.user_name}, Email: {feedback.email}, Subject: {feedback.subject}, Message: {feedback.message}\n")
        print("\nThank you for your feedback!")
    def do_submit_feedback(self, args):
        """
        Submit user feedback.
        Usage: submit_feedback
        """
        self.collect_feedback()

     def do_search_employees(self, args):
        """
        Search employees based on an attribute and value.
        Usage: search_employees <attribute> <value>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help search_employees' for usage.")
            return

        attribute, value = args_list
        result = self.search_employees(attribute, value)
        # Process and display search results

    def do_filter_employees(self, args):
        """
        Filter employees based on custom filters.
        Usage: filter_employees <attribute1=value1> <attribute2=value2> ...
        """
        filters = {}
        for arg in shlex.split(args):
            key, value = arg.split('=')
            filters[key] = value

        result = self.filter_employees(filters)
        # Process and display filter results

    saved_filters = {}

    def save_filter(self, filter_name, filters):
        """Save a custom filter for future use."""
        self.saved_filters[filter_name] = filters

    def do_save_filter(self, args):
        """
        Save a custom filter for future use.
        Usage: save_filter <filter_name> <attribute1=value1> <attribute2=value2> ...
        """
        args_list = shlex.split(args)
        if len(args_list) < 2:
            print("Invalid number of arguments. See 'help save_filter' for usage.")
            return

        filter_name = args_list[0]
        filters = {}
        for arg in args_list[1:]:
            key, value = arg.split('=')
            filters[key] = value

        self.save_filter(filter_name, filters)
        print(f"Filter '{filter_name}' saved successfully!")

     def do_apply_filter(self, args):
        """
        Apply a saved filter.
        Usage: apply_filter <filter_name>
        """
        filter_name = args.strip()
        if filter_name not in self.saved_filters:
            print(f"Filter '{filter_name}' not found.")
            return

        filters = self.saved_filters[filter_name]
        result = self.filter_employees(filters)
        # Process and display filter results

    def do_show_saved_filters(self, args):
        """Show the list of saved filters."""
        if not self.saved_filters:
            print("No saved filters.")
            return

        print("Saved Filters:")
        for filter_name, filters in self.saved_filters.items():
            print(f"{filter_name}: {filters}")


    def do_upload_profile_picture(self, args):
        """
        Upload and update the profile picture for an employee.
        Usage: upload_profile_picture <employee_id> <image_path>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help upload_profile_picture' for usage.")
            return

        employee_id, image_path = args_list
        self.upload_profile_picture(employee_id, image_path)

    def do_preview_profile_picture(self, args):
        """
        Preview the profile picture for an employee.
        Usage: preview_profile_picture <employee_id>
        """
        args_list = shlex.split(args)
        if len(args_list) != 1:
            print("Invalid number of arguments. See 'help preview_profile_picture' for usage.")
            return

        employee_id = args_list[0]
        self.preview_profile_picture(employee_id)

    def do_crop_profile_picture(self, args):
        """
        Crop and update the profile picture for an employee.
        Usage: crop_profile_picture <employee_id> <x> <y> <width> <height>
        """
        args_list = shlex.split(args)
        if len(args_list) != 5:
            print("Invalid number of arguments. See 'help crop_profile_picture' for usage.")
            return

        employee_id, x, y, width, height = args_list
        self.crop_profile_picture(employee_id, int(x), int(y), int(width), int(height))

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
     DATABASE_URL = 'sqlite:///example.db'
    engine = create_engine(DATABASE_URL, echo=True)
    basemodel.Base.metadata.create_all(bind=engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    storage = DBStorage()
    storage.reload()

    console_obj = Console(session, storage)

    while True:
        print("\n--- HR Console ---")
        print("0. Exit")
        print("1. Create Employee")
        print("2. Create Job Opening")
        print("3. Create Company")
        print("4. Show Details")
        print("5. Update Details")
        print("6. Delete Entity")
        print("7. Save to JSON")
        print("8. Load from JSON")
        print("9. Submit Feedback") # new option
        print("10. upload new profile picture") # new option
        print("11. preview profile picture") # new option
        print("12. crop profile picture") # new option

        choice = input("Enter your choice (0-9): ")

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
             #submit user feedback
            console_obj.do_submit_feedback()

         elif choice == '10':
            # Input for uploading profile picture
            employee_id = input("Enter Employee ID: ")
            image_path = input("Enter Image Path: ")
            console_obj.do_upload_profile_picture(f"{employee_id} {image_path}")

        elif choice == '11':
            # Input for previewing profile picture
            employee_id = input("Enter Employee ID: ")
            console_obj.do_preview_profile_picture(employee_id)

        elif choice == '12':
            # Input for cropping profile picture
            employee_id = input("Enter Employee ID: ")
            x = input("Enter X-coordinate: ")
            y = input("Enter Y-coordinate: ")
            width = input("Enter Width: ")
            height = input("Enter Height: ")
            console_obj.do_crop_profile_picture(f"{employee_id} {x} {y} {width} {height}")
             
        elif choice == '0':
            print("Exiting the HR Console. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 9.")
