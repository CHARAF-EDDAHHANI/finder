#!/mnt/d/finder/venv/bin/python

import unittest
from unittest.mock import patch
from io import StringIO
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hr_console.console import Console

# Replace 'sqlite:///test_example.db' with the URL of your test database
TEST_DATABASE_URL = 'sqlite:///test_example.db'
engine = create_engine(TEST_DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
test_session = Session()


class TestConsoleMethods(unittest.TestCase):

    def setUp(self):
        # Create tables in the test database
        test_session.execute('CREATE TABLE IF NOT EXISTS employee (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT, employee_skills TEXT, education TEXT, cv_pdf TEXT, employee_contact TEXT, password TEXT, company_id INTEGER)')
        test_session.execute('CREATE TABLE IF NOT EXISTS job_opening (id INTEGER PRIMARY KEY AUTOINCREMENT, job_title TEXT, location TEXT, recruiter_contact TEXT, job_description TEXT, position_details TEXT, required_skills TEXT, company_id INTEGER)')
        test_session.execute('CREATE TABLE IF NOT EXISTS company (id INTEGER PRIMARY KEY AUTOINCREMENT, company_name TEXT, company_description TEXT, location TEXT, recruiter_contact TEXT)')
        test_session.commit()

        # Redirect stdout to capture print statements
        self.stdout_patch = patch('sys.stdout', new_callable=StringIO)
        self.mock_stdout = self.stdout_patch.start()

    def tearDown(self):
        # Drop tables and close session
        test_session.execute('DROP TABLE IF EXISTS employee')
        test_session.execute('DROP TABLE IF EXISTS job_opening')
        test_session.execute('DROP TABLE IF EXISTS company')
        test_session.commit()
        self.stdout_patch.stop()

    def test_create_employee(self):
        console = Console(test_session)
        console.do_create_employee("John", "Doe", "Programming", "BS in Computer Science", "john_cv.pdf", "john@email.com", "password123", "1")
        self.assertIn("Employee created successfully.", self.mock_stdout.getvalue())

    def test_create_job_opening(self):
        console = Console(test_session)
        console.do_create_job_opening("Software Engineer", "New York", "recruiter@email.com", "Exciting job opportunity", "Details", "Python, JavaScript", "1")
        self.assertIn("Job Opening created successfully.", self.mock_stdout.getvalue())

    def test_create_company(self):
        console = Console(test_session)
        console.do_create_company("ABC Inc.", "Technology company", "San Francisco", "hr@abc.com")
        self.assertIn("Company created successfully.", self.mock_stdout.getvalue())


if __name__ == '__main__':
    unittest.main()
