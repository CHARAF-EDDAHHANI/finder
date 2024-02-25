$(document).ready(function () {
    console.log('App loaded!');
    // Add event listener for the profile dropdown
    $('.profile-dropdown').hover(
        function () {
            // Display dropdown content on hover
            console.log('Dropdown hovered');
            $('.dropdown-content', this).css('display', 'block');
        }
    );

    // Add click event listeners for each option in the dropdown
    $('.dropdown-content a').on('click',
        function () {
            // Handle the click event for each option
            const optionText = $(this).text();
            console.log('Dropdown option clicked:', optionText);

            // Redirect based on the selected option
            switch (optionText) {
                case 'My Profile':
                    console.log('Redirecting to My Profile');
                    window.location.href = 'http://localhost:5000/My_profile';
                    break;
                case 'Add Employee':
                    console.log('Handling Add Employee logic');
                    // Handle the redirect or logic for adding an employee
                    break;
                case 'Post Job':
                    console.log('Handling Post Job logic');
                    // Handle the redirect or logic for posting a job
                    break;
                case 'Feedback':
                    console.log('Handling Feedback logic');
                    // Handle the redirect or logic for providing feedback
                    break;
                default:
                    console.log('Unknown option clicked');
                    // Handle other options if needed
                    break;
            }
        }
    );

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

    // Handling show employee+jobs buttons clicks to show all profiles
    $('#showEmployeesButton').on('click', function () {
        console.log('Show Employees button clicked!');
        // Add logic to fetch and display employees
        displayEmployees();
    });

    $('#showJobsButton').on('click', function () {
        console.log('Show Jobs button clicked!');
        // Add logic to fetch and display jobs
        displayJobs();
    });

    //modaladdemployee
    var modalemployee = $('#infoModal_addemployee');
    var showModaladdemployeebtn = $('#showModaladdemployeebtn');
    var submitBtnemp = $('#submitBtnemp');

    showModaladdemployeebtn.click(function () {
        console.log('Add Employee modal opened');
        modalemployee.css('display', 'block');
    });

    $('.closeemp').click(function () {
        console.log('Add Employee modal closed');
        modalemployee.css('display', 'none');
    });

    submitBtnemp.click(function () {
        console.log('Submit button clicked for Add Employee');
        var first_name = $('#first_name').val();
        var last_name = $('#last_name').val();
        var employee_skills = $('#employee_skills').val();
        var education = $('#education').val();
        var employee_contact = $('#employee_contact').val();

        // Perform AJAX request to send data to the backend
        $.ajax({
            url: 'http://127.0.0.1:5000/create_employee',
            method: 'POST',
            data: { first_name: first_name, last_name: last_name, employee_contact: employee_contact, employee_skills: employee_skills, education: education },
            success: function (response) {
                console.log('Data sent successfully:', response);
                modalemployee.css('display', 'none');
                alert('employee added successfully!');
            },
            error: function (error) {
                console.error('Error sending data:', error);
                alert('Error adding employee. Please try again.');
            }
        });
    });

    //modalpostjob
    var modaljob = $('#infoModal_postjob');
    var showModalpostjobbtn = $('#showModalpostjobbtn');
    var submitBtnjob = $('#submitBtnjob');

    showModalpostjobbtn.click(function() {
        console.log('post job modal opened');
        modaljob.css('display', 'block');
    });

    $('.closejob').click(function() {
        console.log('post job modal closed');
        modaljob.css('display', 'none');
    });

    submitBtnjob.click(function() {
        console.log('submit button for post job clicked');
        var job_title = $('#job_title').val();
        var location = $('#location').val();
        var job_description = $('#job_description').val();
        var recruiter_contact = $('#recruiter_contact').val();

        // Perform AJAX request to send data to the backend
        $.ajax({
            url: 'http://127.0.0.1:5000/create_job',
            method: 'POST',
            data: { job_title : job_title, location : location, job_description: job_description, recruiter_contact : recruiter_contact },
            success: function(response) {
                console.log('Data sent successfully:', response);
                modaljob.css('display', 'none');
                alert('Job created successfully!');
            },
            error: function(error) {
                console.error('Error sending data:', error);
                alert('Error creating job. Please try again.');
            }
        });
    });

    //modalfeedback
    var modalfeedback = $('#infoModal_feedback');
    var showModalfeedbackbtn = $('#showModalfeedbackbtn');
    var submitBtnfeedback = $('#submitBtnfeedback');

    showModalfeedbackbtn.click(function() {
        console.log('feedback modal opened');
        modalfeedback.css('display', 'block');
    });

    $('.closefeedback').click(function() {
        console.log('feedback modal closed')
        modalfeedback.css('display', 'none');
    });

    submitBtnfeedback.click(function() {
        console.log('submit feedback button clicked')
        var user_name = $('#user_name').val();
        var email = $('#email').val();
        var subject = $('#subject').val();
        var message = $('#message').val();

        // Perform AJAX request to send data to the backend
        $.ajax({
            url: 'http://127.0.0.1:5000/submit_feedback',
            method: 'POST',
            data: { user_name : user_name, email : email, subject: subject, message : message },
            success: function(response) {
                console.log('Data sent successfully:', response);
                modalfeedback.css('display', 'none');
                alert('feedback submitted successfully!');
            },
            error: function(error) {
                console.error('Error sending data:', error);
                alert('Error submitting feedback. Please try again.');
            }
        });
    });
////////
});

