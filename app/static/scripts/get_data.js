$(document).ready(function () {
    // Function to fetch and display employees
    function displayEmployees() {
        console.log('Fetching employee data from the backend...');
        // Perform AJAX request to fetch employee data from the backend
        $.ajax({
            url: 'http://127.0.0.1:5000/get_employees',
            method: 'GET',
            success: function (response) {
                console.log('Employee data fetched successfully:', response);

        // Display employees in the slides
        const employeesSlides = $('#employeeSlides');
            employeesSlides.empty(); // Clear existing content

            response.forEach(employee => {
                const slide = $('<div>').addClass('slide');
                slide.text(`${employee.first_name} ${employee.last_name}\nSkills: ${employee.employee_skills}\nEducation: ${employee.education}`);
                employeesSlides.append(slide);
            });
        },
        error: function (error) {
            console.error('Error fetching employee data:', error);
        }
    });
  }

// Function to fetch and display jobs
function displayJobs() {
    console.log('Fetching job data from the backend...');
    // Perform AJAX request to fetch job data from the backend
    $.ajax({
        url: 'http://127.0.0.1:5000/get_jobs',
        method: 'GET',
        success: function (response) {
            console.log('Job data fetched successfully:', response);

            // Display jobs in the slides
            const jobsSlides = $('#jobsSlides');
            jobsSlides.empty(); // Clear existing content

            response.forEach(job => {
                const slide = $('<div>').addClass('slide');
                slide.text(`${job.job_title}\nLocation: ${job.location}\nContact: ${job.recruiter_contact}\nDescription: ${job.job_description}`);
                jobsSlides.append(slide);
            });
        },
        error: function (error) {
            console.error('Error fetching job data:', error);
        }
    });
  }
});
