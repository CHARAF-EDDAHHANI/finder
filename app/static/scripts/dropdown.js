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
                    console.log(' create new employee');
                    // Handle the redirect or logic for adding an employee
                    break;
                case 'Post Job':
                    console.log('create new Job');
                    // Handle the redirect or logic for posting a job
                    break;
                case 'Feedback':
                    console.log('submit  Feedback');
                    // Handle the redirect or logic for providing feedback
                    break;
                default:
                    console.log('Unknown option clicked');
                    // Handle other options if needed
                    break;
            }
        }
    );

}
);
