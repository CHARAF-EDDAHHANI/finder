$(document).ready(function () {
    console.log('App loaded!');
    // Add event listener for the profile dropdown
    $('.profile-dropdown').hover(
    function () {
        // Display dropdown content on hover
        $('.dropdown-content', this).css('display', 'block');
        });

    // Add click event listeners for each option in the dropdown
    $('.dropdown-content a').on('click',
    function () {
        // Handle the click event for each option
        const optionText = $(this).text();
        // Redirect based on the selected option
    switch (optionText) {
        case 'My Profile':
            window.location.href = 'http://localhost:5000/My_profile';
            break;
        case 'Add Employee':
            // Handle the redirect or logic for adding an employee
            break;
        case 'Post Job':
            // Handle the redirect or logic for posting a job
            break;
        case 'Feedback' :
            //handle the redirect or logic for providing  feedback
        default:
            // Handle other options if needed
            break;
    }

    });

    // Function to fetch and display employees
    function displayEmployees() {
    // Perform AJAX request to fetch employee data from the backend
    $.ajax({
        url: 'http://34.229.68.97:5000/get_employees',
        method: 'GET',
        success: function(response) {
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
        error: function(error) {
            console.error('Error fetching employee data:', error);
        }
    });
    }

    // Function to fetch and display jobs
    function displayJobs() {
        // Perform AJAX request to fetch job data from the backend
        $.ajax({
            url: 'http://34.229.68.97:5000/get_jobs',
            method: 'GET',
            success: function(response) {
                console.log('Job data fetched successfully:', response);
    
                // Display jobs in the slides
                const jobsSlides = $('#jobsSlides');
                jobsSlides.empty(); // Clear existing content
    
                response.forEach(job => {
                    const slide = $('<div>').addClass('slide');
                    // Correct variable names here
                    slide.text(`${job.job_title}\nLocation: ${job.location}\nContact: ${job.recruiter_contact}\nDescription: ${job.job_description}`);
                    jobsSlides.append(slide);
                });
            },
            error: function(error) {
                console.error('Error fetching job data:', error);
            }
        });
    }    

    
//handling show employee+jobs buttons clicks to show all profiles
    $('#showEmployeesButton').on('click', function () {
        console.log('Show Employees button clicked!');
        // Add logic to fetch and display employees
    });

    $('#showJobsButton').on('click', function () {
        console.log('Show Jobs button clicked!');
        // Add logic to fetch and display jobs
    });
    //modaladdemployee
    var modalemployee = $('#infoModal_addemployee');
    var showModaladdemployeebtn = $('#showModaladdemployeebtn');
    var submitBtnemp = $('#submitBtnemp');

    showModaladdemployeebtn.click(function() {
        modalemployee.css('display', 'block');
    });

    $('.closeemp').click(function() {
        modalemployee.css('display', 'none');
    });

    submitBtnemp.click(function() {
        var Fisrt_name = $('#First_name').val();
        var Last_name = $('#Last_name').val();
        var Employee_skills = $('#Employee_skills').val();
        var Education = $('#Education').val();
        var Employee_contact = $('#Employee_contact').val();

        // Perform AJAX request to send data to the backend
        $.ajax({
            url: 'http://34.229.68.97:5000/create_employee',
            method: 'POST',
            data: { Fisrt_name : Fisrt_name, Last_name : Last_name, Employee_contact : Employee_contact, Employee_skills : Employee_skills, Education : Education },
            success: function(response) {
                console.log('Data sent successfully:', response);
                modalemployee.css('display', 'none');
                alert('employee added successfullu!');
            },
            error: function(error) {
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
        modaljob.css('display', 'block');
    });

    $('.closejob').click(function() {
        modaljob.css('display', 'none');
    });

    submitBtnjob.click(function() {
        var Job_title = $('#Job_title').val();
        var Location = $('#Location').val();
        var Job_description = $('#Job_description').val();
        var Recruiter_contact = $('#Recruiter_contact').val();

        // Perform AJAX request to send data to the backend
        $.ajax({
            url: 'http://34.229.68.97:5000/',
            method: 'POST',
            data: { Job_title : Job_title, Location : Location, Job_description: Job_description, Recruiter_contact : Recruiter_contact },
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
        modalfeedback.css('display', 'block');
    });

    $('.closefeedback').click(function() {
        modalfeedback.css('display', 'none');
    });

    submitBtnfeedback.click(function() {
        var user_name = $('#user_name').val();
        var email = $('#email').val();
        var subject = $('#subject').val();
        var message = $('#message').val();

        // Perform AJAX request to send data to the backend
        $.ajax({
            url: 'http://34.229.68.97:5000/',
            method: 'POST',
            data: { user_name : user_name, email : email, subject: subject, Recruiter_contact : message },
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

