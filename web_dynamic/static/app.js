$(document).ready(function () {
    console.log('App loaded!');
    // Add event listener for the profile dropdown
    $('.profile-dropdown').hover(
    function () {
        // Display dropdown content on hover
        $('.dropdown-content', this).css('display', 'block');
        }, 
    function () {
        // Hide dropdown content when not hovering
        $('.dropdown-content', this).css('display', 'none');
    });

    // Add click event listeners for each option in the dropdown
    $('.dropdown-content a').on('click',
    function () {
        // Handle the click event for each option
        const optionText = $(this).text();
        // Redirect based on the selected option
    switch (optionText) {
        case 'My Profile':
            window.location.href = 'user-profile-url';
            break;
        case 'Add Employee':
            // Handle the redirect or logic for adding an employee
            break;
        case 'Post Jobs':
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
        // Mock data (replace with actual API call)
        const employeesData = [
            { first_name: 'John', last_name: 'Doe', employee_skills: 'JavaScript, HTML, CSS', education: 'Bachelor\'s in Computer Science' },
            // Add more employee data as needed
        ];

        // Display employees in the slides
        const employeesSlides = $('#employeeSlides');
        employeesSlides.empty(); // Clear existing content

        employeesData.forEach(employee => {
            const slide = $('<div>').addClass('slide');
            slide.text(`${employee.first_name} ${employee.last_name}\nSkills: ${employee.employee_skills}\nEducation: ${employee.education}`);
            employeesSlides.append(slide);
        });
    }

   
    // Function to fetch and display jobs
    function displayJobs() {
        // Mock data (replace with actual API call)
        const jobsData = [
            { job_title: 'Software Engineer', location: 'City B', recruiter_contact: 'recruiterB@example.com', job_description: 'Full-stack development' },
            // Add more jobs data as needed
        ];

        // Display jobs in the slides
        const jobsSlides = $('#jobsSlides');
        jobsSlides.empty(); // Clear existing content

        jobsData.forEach(job => {
            const slide = $('<div>').addClass('slide');
            slide.text(`${job.job_title}\nLocation: ${jobs.location}\nContact: ${jobOpening.recruiter_contact}\nDescription: ${jobOpening.job_description}`);
            jobsSlides.append(slide);
        });
    }
    
//handling show employee+job+comp buttons clicks to show all profiles
    $('#showEmployeesButton').on('click', function () {
        console.log('Show Employees button clicked!');
        // Add logic to fetch and display employees
    });

    $('#showJobsButton').on('click', function () {
        console.log('Show Jobs button clicked!');
        // Add logic to fetch and display jobs
    });
    });
