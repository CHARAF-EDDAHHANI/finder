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
        case 'Post Job Opening':
            // Handle the redirect or logic for posting a job opening
            break;
        case 'Add Company':
            // Handle the redirect or logic for adding a company
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

    // Function to fetch and display companies
    function displayCompanies() {
        // Mock data (replace with actual API call)
        const companiesData = [
            { company_name: 'Company A', company_description: 'Tech Company', location: 'City A', recruiter_contact: 'recruiterA@example.com' },
            // Add more company data as needed
        ];

        // Display companies in the slides
        const companiesSlides = $('#companySlides');
        companiesSlides.empty(); // Clear existing content

        companiesData.forEach(company => {
            const slide = $('<div>').addClass('slide');
            slide.text(`${company.company_name}\nDescription: ${company.company_description}\nLocation: ${company.location}\nContact: ${company.recruiter_contact}`);
            companiesSlides.append(slide);
        });
    }

    // Function to fetch and display job openings
    function displayJobOpenings() {
        // Mock data (replace with actual API call)
        const jobOpeningsData = [
            { job_title: 'Software Engineer', location: 'City B', recruiter_contact: 'recruiterB@example.com', job_description: 'Full-stack development' },
            // Add more job opening data as needed
        ];

        // Display job openings in the slides
        const jobOpeningsSlides = $('#jobOpeningSlides');
        jobOpeningsSlides.empty(); // Clear existing content

        jobOpeningsData.forEach(jobOpening => {
            const slide = $('<div>').addClass('slide');
            slide.text(`${jobOpening.job_title}\nLocation: ${jobOpening.location}\nContact: ${jobOpening.recruiter_contact}\nDescription: ${jobOpening.job_description}`);
            jobOpeningsSlides.append(slide);
        });
    }

    // Example: Handling a button click to display employees
    const employeesButton = $('#employeesButton');
    if (employeesButton.length) {
        employeesButton.on('click', function () {
            displayEmployees();
        });

//handling show employee+job+comp buttons clicks to show all profiles
    $('#showEmployeesButton').on('click', function () {
        console.log('Show Employees button clicked!');
        // Add logic to fetch and display employees
    });

    $('#showCompaniesButton').on('click', function () {
        console.log('Show Companies button clicked!');
        // Add logic to fetch and display companies
    });

    $('#showJobOpeningsButton').on('click', function () {
        console.log('Show Job Openings button clicked!');
        // Add logic to fetch and display job openings
    });

    // ... More button click handlers ...

    // Example: Handling a button click for interaction with the backend
    const interactionButton = $('#interactionButton');
    if (interactionButton.length) {
        interactionButton.on('click', function () {
            console.log('Button clicked!');
            // Add your logic here
        });
    }
});
