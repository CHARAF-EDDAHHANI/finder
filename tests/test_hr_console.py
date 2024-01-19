import unittest
from hr_console import basemodel, console, employee, jobopening, company
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class HRConsoleTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Set up the test database and session
        cls.engine = create_engine('sqlite:///:memory:', echo=True)
        basemodel.Base.metadata.create_all(bind=cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)
        cls.session = cls.Session()

    @classmethod
    def tearDownClass(cls):
        # Clean up resources after all tests
        cls.session.close()

    def test_create_employee(self):
        # Test creating an employee
        console_obj = console.Console(session=self.session)
        console_obj.create_employee('John', 'Doe', 'Programming', 'Computer Science', 'john_cv.pdf', 'john@example.com', 'password123')
        result = self.session.query(employee.Employee).filter_by(first_name='John').first()
        self.assertIsNotNone(result)

    def test_create_job_opening(self):
        # Test creating a job opening
        console_obj = console.Console(session=self.session)
        console_obj.create_job_opening('Software Engineer', 'City', 'recruiter@example.com', 'Description', 'Details', 'Python, JavaScript')
        result = self.session.query(jobopening.JobOpening).filter_by(job_title='Software Engineer').first()
        self.assertIsNotNone(result)

    def test_create_company(self):
        # Test creating a company
        console_obj = console.Console(session=self.session)
        console_obj.create_company('Tech Corp', 'Tech Company', 'City', 'recruiter@example.com')
        result = self.session.query(company.Company).filter_by(company_name='Tech Corp').first()
        self.assertIsNotNone(result)

if __name__ == '__main__':
    unittest.main()
