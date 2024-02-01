$(document).ready(function () {
    // Function to create an employee
    function createEmployee(data) {
      $.ajax({
        url: 'http://localhost:5000/create_employee',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(data),
        success: function (data) {
          console.log('Success:', data);
          // Handle success, update UI, etc.
        },
        error: function (error) {
          console.error('Error:', error);
          // Handle errors
        }
      });
    }

    // Example: Trigger the createEmployee function with sample data
    const employeeData = {
      first_name: 'John',
      last_name: 'Doe',
      employee_skills: 'Programming',
      education: 'Bachelor',
      cv_pdf: 'path/to/cv.pdf',
      employee_contact: 'john@example.com',
      password: 'securepassword',
      company_id: 1,  // Set the company_id as needed
    };

    createEmployee(employeeData);
  });