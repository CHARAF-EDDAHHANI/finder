import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from hr_console import basemodel, console, employee, jobopening, company
from filestorage import FileStorage

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

    def setUp(self):
        # Clear the session before each test
        self.session.query(employee.Employee).delete()
        self.session.query(jobopening.JobOpening).delete()
        self.session.query(company.Company).delete()
        self.session.commit()

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

    def test_save_load_json(self):
        # Test saving and loading instances to/from JSON
        console_obj = console.Console(session=self.session)
        console_obj.create_employee('Alice', 'Johnson', 'Data Science', 'Mathematics', 'alice_cv.pdf', 'alice@example.com', 'password456')
        console_obj.create_job_opening('Data Engineer', 'Remote', 'hr@example.com', 'Job Description', 'Remote Position', 'SQL, Python')
        console_obj.create_company('Data Corp', 'Data-Driven Company', 'City X', 'hr@example.com')

        # Save instances to JSON
        console_obj.save_to_json(employee.Employee, 'test_employees.json')
        console_obj.save_to_json(jobopening.JobOpening, 'test_job_openings.json')
        console_obj.save_to_json(company.Company, 'test_companies.json')

        # Clear the session to avoid conflicts when loading from JSON
        self.session.expunge_all()

        # Load instances from JSON
        console_obj.load_from_json(employee.Employee, 'test_employees.json')
        console_obj.load_from_json(jobopening.JobOpening, 'test_job_openings.json')
        console_obj.load_from_json(company.Company, 'test_companies.json')

        # Check if instances were loaded successfully
        loaded_employee = self.session.query(employee.Employee).filter_by(first_name='Alice').first()
        loaded_job_opening = self.session.query(jobopening.JobOpening).filter_by(job_title='Data Engineer').first()
        loaded_company = self.session.query(company.Company).filter_by(company_name='Data Corp').first()

        self.assertIsNotNone(loaded_employee)
        self.assertIsNotNone(loaded_job_opening)
        self.assertIsNotNone(loaded_company)

if __name__ == '__main__':
    unittest.main()
