$(document).ready(function () {

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


    
    

    