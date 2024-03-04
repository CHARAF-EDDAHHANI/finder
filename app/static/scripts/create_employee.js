$(document).ready(function () {

    // Select the submit button by ID
    var submitBtnemp = $('#submitBtnemp');

    // Add a click event listener to the submit button
    submitBtnemp.click(function () {
        var formData = new FormData(employeeForm);
        console.log('Submit button clicked for Add Employee');

        // Extract data from form fields
        var first_name = $('#first_name').val();
        var last_name = $('#last_name').val();
        var employee_skills = $('#employee_skills').val();
        var education = $('#education').val();
        var employee_contact = $('#employee_contact').val();
        var photo = $('#photo').val();

        // Perform AJAX request to send data to the backend
        $.ajax({
            type: 'POST',
            url: '/create_employee',
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log('Data sent successfully:', response);
                $('#modalemployee').css('display', 'none');
                alert('Employee added successfully!');
            },
            error: function (error) {
                console.error('Error sending data:', error);
                alert('Error adding employee. Please try again.');
            }
        });
    });
});
