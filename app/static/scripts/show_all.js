$(document).ready(function () {

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

});