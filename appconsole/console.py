#!/usr/bin/env python3

import sys
import cmd
import shlex
import json
from sqlalchemy import or_, func
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from PIL import Image
from employee import Employee
from jobs import JobOpening
from feedback import Feedback
from appengine.filestorage import FileStorage
from appengine.db_storage import DBStorage
import basemodel

DATABASE_URL = 'sqlite:///appengine/finder.db'  # Update the path to your finder.db
engine = create_engine(DATABASE_URL, echo=True)
basemodel.Base.metadata.create_all(bind=engine)
Session = sessionmaker(bind=engine)
session = Session()
storage = DBStorage()
storage.reload()

class Console(cmd.Cmd):
    intro = "Welcome to the HR Console. Type 'help' to list available commands."
    prompt = "(HR Console) "

    def __init__(self, session, storage, another_argument=None):
        super().__init__()
        self.session = session
        self.storage = storage

    def create_employee(self, first_name, last_name, employee_skills, education, employee_contact):
        try:
            # Validate input types or any other conditions here

            employee = Employee(first_name=first_name, last_name=last_name, employee_skills=employee_skills,
                            education=education, employee_contact=employee_contact)
            self.session.add(employee)
            self.session.commit()
            print("Employee created successfully.")
        except Exception as e:
            print(f"Error creating employee: {e}")

    def do_create_employee(self, args):
        """
        Create a new employee.
        Usage: create_employee <first_name> <last_name> <employee_skills> <education>  <employee_contact>
        """
        args_list = shlex.split(args)
        if len(args_list) < 5:
            print("Invalid number of arguments. See 'help create_employee' for usage.")
            return

        self.create_employee(*args_list)

    def do_create_job_opening(self, args):
        """
        Create a new job opening.
        Usage: create_job_opening <job_title> <location> <recruiter_contact> <job_description>
        """
        args_list = shlex.split(args)
        if len(args_list) < 4:
            print("Invalid number of arguments. See 'help create_job_opening' for usage.")
            return

        self.create_job_opening(*args_list)

    def create_job_opening(self, Job_title, Location, Recruiter_contact, Job_description):
        try:
            # Validate input types or any other conditions here

            job_opening = JobOpening(Job_title=Job_title, Location=Location, Recruiter_contact=Recruiter_contact,
                                Job_description=Job_description)
            self.session.add(job_opening)
            self.session.commit()
            print("Job Opening created successfully.")
        except Exception as e:
            print(f"Error creating job opening: {e}")

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
        employee = self.session.query(Employee).filter(
            or_(
                func.concat(Employee.first_name, ' ', Employee.last_name) == profile_name,
                Employee.first_name == profile_name,
                Employee.last_name == profile_name
            )
        ).first()

        if employee:
            print(f"Employee Details:\nFirst Name: {employee.first_name}\nLast Name: {employee.last_name}\n"
                f"Skills: {employee.employee_skills}\nEducation: {employee.education}\n"
                f"Contact: {employee.employee_contact}")
            return

        # Check if the profile_name corresponds to a job opening
        job_opening = self.session.query(JobOpening).filter(JobOpening.job_title == profile_name).first()

        if job_opening:

            print(f"Job Opening Details:\nJob Title: {job_opening.Job_title}\nLocation: {job_opening.Location}\n"
                f"Recruiter Contact: {job_opening.Recruiter_contact}\nDescription: {job_opening.Job_description}")
        else:
            print(f"No profile found for {profile_name}")

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

        if profile_type.lower() == 'employee':
            self.update_employee(profile_type, attribute_name, new_value)
        elif profile_type.lower() == 'jobopening':
            self.update_job_opening(profile_type, attribute_name, new_value)
        else:
            print(f"Invalid profile type: {profile_type}")

    def update_employee(self, profile_type, attribute_name, new_value):
        try:
            # Validate input types or any other conditions here
            # Retrieve the employee based on the profile name
            employee = self.session.query(Employee).filter(
                or_(
                    func.concat(Employee.first_name, ' ', Employee.last_name) == profile_type,
                    Employee.first_name == profile_type,
                    Employee.last_name == profile_type
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

    def update_job_opening(self, profile_type, attribute_name, new_value):
        try:
            # Validate input types or any other conditions here
            # Retrieve the job opening based on the profile name
            job_opening = self.session.query(JobOpening).filter(JobOpening.Job_title == profile_type).first()

            if not job_opening:
                print(f"No job opening found with title {profile_type}")
                return

            # Update the specified attribute with the new value
            if attribute_name.lower() == 'Job_title':
                job_opening.Job_title = new_value
            else:
                print(f"Invalid attribute name for job opening: {attribute_name}")
                return

            self.session.commit()
            print("Job Opening details updated successfully.")
        except Exception as e:
            print(f"Error updating job opening details: {e}")

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

        if profile_type.lower() == 'employee':
            self.delete_employee(profile_name)
        elif profile_type.lower() == 'jobopening':
            self.delete_job_opening(profile_name)
        else:
            print(f"Invalid profile type: {profile_type}")

    def delete_employee(self, profile_name):
        try:
            # Retrieve the employee based on the profile name
            employee = self.session.query(Employee).filter(
                or_(
                    func.concat(Employee.first_name, ' ', Employee.last_name) == profile_name,
                    Employee.first_name == profile_name,
                    Employee.last_name == profile_name
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

    def delete_job_opening(self, profile_name):
        try:
            # Retrieve the job opening based on the profile name
            job_opening = self.session.query(JobOpening).filter(JobOpening.Job_title == profile_name).first()

            if job_opening:
                self.session.delete(job_opening)
                self.session.commit()
                print(f"Job Opening with title {profile_name} deleted successfully.")
            else:
                print(f"No job opening found with title {profile_name}")
        except Exception as e:
            print(f"Error deleting job opening: {e}")

    # Exit console
    def do_exit(self, args):
        """
        Exit the HR Console.
        """
        print("Exiting HR Console. Goodbye!")
        return True

    def save_to_json(self, class_type, filename):
        objects = self.session.query(class_type).all()
        FileStorage.save_to_json(objects, filename)

    def load_from_json(self, class_type, filename):
        objects = FileStorage.load_from_json(class_type, filename)
        for obj in objects:
            self.session.add(obj)
        self.session.commit()

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


if __name__ == "__main__":
    console_obj = Console(session, storage)

    while True:
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

        choice = input("Enter your choice (0-8): ")

        if choice == '1':
            # Input for creating an employee
            first_name = input("Enter First Name: ")
            last_name = input("Enter Last Name: ")
            employee_skills = input("Enter Employee Skills: ")
            education = input("Enter Education: ")
            employee_contact = input("Enter Employee Contact: ")

            console_obj.create_employee(first_name, last_name, employee_skills, education, employee_contact)

        elif choice == '2':
            # Input for creating a job
            Job_title = input("Enter Job Title: ")
            Location = input("Enter Location: ")
            Recruiter_contact = input("Enter Recruiter Contact: ")
            Job_description = input("Enter Job Description: ")

            console_obj.create_job_opening(job_title, location, recruiter_contact, job_description)

        elif choice == '3':
            # Input for showing details
            profile_type = input("Enter profile type (Employee/JobOpening): ")
            profile_name = input("Enter profile name: ")
            console_obj.do_show(f"{profile_type} {profile_name}")

        elif choice == '4':
            # Input for updating details
            profile_type = input("Enter profile type (Employee/JobOpening): ")
            profile_name = input("Enter profile name: ")
            attribute_name = input("Enter Attribute Name: ")
            new_value = input("Enter New Value: ")
            console_obj.do_update(f"{profile_type} {profile_name} {attribute_name} {new_value}")

        elif choice == '5':
            # Input for deleting an entity
            profile_type = input("Enter profile type (Employee/JobOpening): ")
            profile_name = input("Enter profile name: ")
            console_obj.do_delete(f"{profile_type} {profile_name}")

        elif choice == '6':
            # Submit user feedback
            console_obj.do_submit_feedback('')

        elif choice == '7':
            # Input for saving to JSON
            class_type = input("Enter Class Type (Employee/JobOpening): ")
            filename = input("Enter Filename: ")
            console_obj.do_save_to_json(f"{class_type} {filename}")

        elif choice == '8':
            # Input for loading from JSON
            class_type = input("Enter Class Type (Employee/JobOpening): ")
            filename = input("Enter Filename: ")
            console_obj.do_load_from_json(f"{class_type} {filename}")

        elif choice == '0':
            print("Exiting the HR Console. Goodbye!")
            break

        else:
            print("Invalid choice. Please enter a number between 1 and 8.")
