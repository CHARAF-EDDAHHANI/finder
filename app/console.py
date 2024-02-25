#!/usr/bin/env python3

import sys
import cmd
import shlex
from sqlalchemy import or_, func
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from employees import employeemodel
from jobs import jobmodel
from feedback import feedbackmodel
from appengine.filestorage import FileStorage
from appengine.db_storage import DBStorage
import basemodel

# Define the database URL and create the engine
DATABASE_URL = 'sqlite:///appengine/app.db'  # Update the path to db
engine = create_engine(DATABASE_URL, echo=True)

# Create tables based on the defined models
basemodel.Base.metadata.create_all(bind=engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Create storage instances for file and database storage
storage = DBStorage()
storage.reload()

# Console class for handling user commands
class Console(cmd.Cmd):
    intro = "Welcome to the HR Console. Type 'help' to list available commands."
    prompt = "(HR Console) "

    def __init__(self, session, storage, another_argument=None):
        super().__init__()
        self.session = session
        self.storage = storage

    # Method to create a new employee
    def create_employee(self, first_name, last_name, employee_skills, education, employee_contact):
        try:
            # Create an instance of the employeemodel and add it to the session
            employee = employeemodel(
                first_name=first_name,
                last_name=last_name,
                employee_skills=employee_skills,
                education=education,
                employee_contact=employee_contact
            )
            self.session.add(employee)
            self.session.commit()
            print("Employee created successfully.")
        except Exception as e:
            print(f"Error creating employee: {e}")

    # Method to create a new job 
    def create_job(self, job_title, location, recruiter_contact, job_description):
        try:
            # Create an instance of the jobmodel and add it to the session
            job = jobmodel(
                job_title=job_title,
                location=location,
                recruiter_contact=recruiter_contact,
                job_description=job_description
            )
            self.session.add(job)
            self.session.commit()
            print("Job created successfully.")
        except Exception as e:
            print(f"Error creating job : {e}")

    # Command to create an employee from the console
    def do_create_employee(self, args):
        """
        Create a new employee.
        Usage: create_employee <first_name> <last_name> <employee_skills> <education> <employee_contact>
        """
        args_list = args.split()
        if len(args_list) < 5:
            print("Invalid number of arguments. See 'help create_employee' for usage.")
            return

        self.create_employee(*args_list)

    # Command to create a job opening from the console
    def do_create_job(self, args):
        """
        Create a new job.
        Usage: create_job <job_title> <location> <recruiter_contact> <job_description>
        """
        args_list = shlex.split(args)
        if len(args_list) < 4:
            print("Invalid number of arguments. See 'help create_job_opening' for usage.")
            return

        self.create_job(*args_list)

    # Command to show details of an entity (employee or job)
    def do_show(self, args):
        """
        Show details of an entity.
        Usage: show <profile name>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help show' for usage.")
            return

        profile_name = args_list[1]

        # Check if the profile_name corresponds to an employee
        employee = self.session.query(employeemodel).filter(
            or_(
                func.concat(employeemodel.first_name, ' ', employeemodel.last_name) == profile_name,
                employeemodel.first_name == profile_name,
                employeemodel.last_name == profile_name
            )
        ).first()

        if employee:
            print(f"Employee Details:\nFirst Name: {employee.first_name}\nLast Name: {employee.last_name}\n"
                  f"Skills: {employee.employee_skills}\nEducation: {employee.education}\n"
                  f"Contact: {employee.employee_contact}")
            return

        # Check if the profile_name corresponds to a job
        job = self.session.query(jobmodel).filter(jobmodel.job_title == profile_name).first()

        if job:
            print(f"Job Details:\nJob Title: {job.job_title}\nLocation: {job.location}\n"
                  f"Recruiter Contact: {job.recruiter_contact}\nDescription: {job.job_description}")
        else:
            print(f"No profile found for {profile_name}")

     # Command to update details of a profile (employee or job)
    def do_update(self, args):
        """
        Update details of a profile.
        Usage: update <profile type>  <attribute_name> <new_value>
        """
        args_list = shlex.split(args)
        if len(args_list) != 3:
            print("Invalid number of arguments. See 'help update' for usage.")
            return

        profile_type = args_list[0]
        attribute_name = args_list[1]
        new_value = args_list[2]

        if profile_type.lower() == 'employeemodel':
            self.update_employee(profile_type, attribute_name, new_value)
        elif profile_type.lower() == 'jobmodel':
            self.update_job_opening(profile_type, attribute_name, new_value)
        else:
            print(f"Invalid profile type: {profile_type}")

    # Method to update details of an employee
    def update_employee(self, profile_type, attribute_name, new_value):
        try:
            # Retrieve the employee based on the profile name
            employee = self.session.query(employeemodel).filter(
                or_(
                    func.concat(employeemodel.first_name, ' ', employeemodel.last_name) == profile_type,
                    employeemodel.first_name == profile_type,
                    employeemodel.last_name == profile_type
                )
            ).first()

            if not employee:
                print(f"No employee found with name {profile_type}")
                return

            # Update the specified attribute with the new value
            if attribute_name.lower() == 'first_name':
                employee.first_name = new_value
            elif attribute_name.lower() == 'last_name':
                employee.last_name = new_value
            else:
                print(f"Invalid attribute name for employee: {attribute_name}")
                return

            self.session.commit()
            print("Employee details updated successfully.")
        except Exception as e:
            print(f"Error updating employee details: {e}")

    # Method to update details of a job 
    def update_job(self, profile_type, attribute_name, new_value):
        try:
            # Retrieve the job based on the profile name
            job = self.session.query(jobmodel).filter(jobmodel.job_title == profile_type).first()

            if not job :
                print(f"No job opening found with title {profile_type}")
                return

            # Update the specified attribute with the new value
            if attribute_name.lower() == 'job_title':
                job.job_title = new_value
            else:
                print(f"Invalid attribute name for job : {attribute_name}")
                return

            self.session.commit()
            print("Job details updated successfully.")
        except Exception as e:
            print(f"Error updating job details: {e}")

     # Command to delete a profile (employee or job)
    def do_delete(self, args):
        """
        Delete a profile.
        Usage: delete <profile type> <profile name>
        """
        args_list = shlex.split(args)
        if len(args_list) != 2:
            print("Invalid number of arguments. See 'help delete' for usage.")
            return

        profile_type = args_list[0]
        profile_name = args_list[1]

        if profile_type.lower() == 'employees':
            self.delete_employee(profile_name)
        elif profile_type.lower() == 'jobs':
            self.delete_job_opening(profile_name)
        else:
            print(f"Invalid profile type: {profile_type}")

    # Method to delete an employee
    def delete_employee(self, profile_name):
        try:
            # Retrieve the employee based on the profile name
            employee = self.session.query(employeemodel).filter(
                or_(
                    func.concat(employeemodel.first_name, ' ', employeemodel.last_name) == profile_name,
                    employeemodel.first_name == profile_name,
                    employeemodel.last_name == profile_name
                )
            ).first()

            if employee:
                self.session.delete(employee)
                self.session.commit()
                print(f"Employee with name {profile_name} deleted successfully.")
            else:
                print(f"No employee found with name {profile_name}")
        except Exception as e:
            print(f"Error deleting employee: {e}")

     # Method to delete a job
    def delete_job(self, profile_name):
        try:
            # Retrieve the job based on the profile name
            job = self.session.query(jobmodel).filter(jobmodel.job_title == profile_name).first()

            if job:
                self.session.delete(job)
                self.session.commit()
                print(f"Job  with title {profile_name} deleted successfully.")
            else:
                print(f"No job  found with title {profile_name}")
        except Exception as e:
            print(f"Error deleting job : {e}")

    # command to Exit console
    def do_exit(self, args):
        """
        Exit the HR Console.
        """
        print("Exiting HR Console. Goodbye!")
        return True

    # Method to save instances to a JSON file
    def save_to_json(self, class_type, filename):
        objects = self.session.query(class_type).all()
        FileStorage.save_to_json(objects, filename)

    # Method to load instances from a JSON file
    def load_from_json(self, class_type, filename):
        objects = FileStorage.load_from_json(class_type, filename)
        for obj in objects:
            self.session.add(obj)
        self.session.commit()

    # Method to collect and store user feedback
    def collect_feedback(self):
        print("\nEnter your feedback:")
        user_name = input("Your Name: ")
        email = input("Your Email: ")
        subject = input("Feedback Subject: ")
        message = input("Your Feedback: ")

        feedback = feedbackmodel(user_name, email, subject, message)
        # Optionally, we can save the feedback to a file or database for future review.
        with open('feedback.txt', 'a') as feedback_file:
            feedback_file.write(f"Name: {feedback.user_name}, Email: {feedback.email}, Subject: {feedback.subject}, Message: {feedback.message}\n")
        print("\nThank you for your feedback!")

    # Command to submit user feedback
    def do_submit_feedback(self, args):
        """
        Submit user feedback.
        Usage: submit_feedback
        """
        self.collect_feedback()

    # Command to save instances to a JSON file
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

    # Command to load instances from a JSON file
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

# Main execution block
if __name__ == "__main__":
    console_obj = Console(session, storage)

    while True:
        # Display the console menu
        print("\n--- HR Console ---")
        print("0. Exit")
        print("1. Create Employee")
        print("2. Create Job")
        print("3. Show Details")
        print("4. Update Details")
        print("5. Delete existing profile")
        print("6. Save to JSON")
        print("7. Load from JSON")
        print("8. Submit Feedback")

        # Prompt user for choice
        choice = input("Enter your choice (0-8): ")

        # Execute the chosen command
        if choice == '1':
            # Input for creating an employee
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            employee_skills = input("Enter Employee Skills: ")
            education = input("Enter Education: ")
            employee_contact = input("Enter Employee Contact: ")

            console_obj.create_employee(first_name, last_name, employee_skills, education, employee_contact)

        # Input for creating a job 
        elif choice == '2':
            # Input for creating a job
            job_title = input("Enter Job Title: ")
            location = input("Enter Location: ")
            recruiter_contact = input("Enter Recruiter Contact: ")
            job_description = input("Enter Job Description: ")

            console_obj.create_job(job_title, location, recruiter_contact, job_description)

        elif choice == '3':
            # Input for showing details
            profile_type = input("Enter profile type (Employee/Job): ")
            profile_name = input("Enter profile name: ")
            console_obj.do_show(f"{profile_type} {profile_name}")

        elif choice == '4':
            # Input for updating details
            profile_type = input("Enter profile type (Employee/Job): ")
            profile_name = input("Enter profile name: ")
            attribute_name = input("Enter Attribute Name: ")
            new_value = input("Enter New Value: ")
            console_obj.do_update(f"{profile_type} {profile_name} {attribute_name} {new_value}")

        elif choice == '5':
            # Input for deleting an entity
            profile_type = input("Enter profile type (Employee/Job): ")
            profile_name = input("Enter profile name: ")
            console_obj.do_delete(f"{profile_type} {profile_name}")

        elif choice == '8':
            # Submit user feedback
            console_obj.do_submit_feedback('')

        elif choice == '6':
            # Input for saving to JSON
            class_type = input("Enter Class Type (Employee/Job): ")
            filename = input("Enter Filename: ")
            console_obj.do_save_to_json(f"{class_type} {filename}")

        elif choice == '7':
            # Input for loading from JSON
            class_type = input("Enter Class Type (Employee/Job): ")
            filename = input("Enter Filename: ")
            console_obj.do_load_from_json(f"{class_type} {filename}")

        elif choice == '0':
            print("Exiting the HR Console. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
