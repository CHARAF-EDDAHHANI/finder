$(document).ready(function () {
    // Your jQuery code here
    console.log('App loaded!');

    // Add event listeners or other logic as needed

    // Example: Handling a button click
    const myButton = $('#searchButton');
    if (myButton.length) {
        myButton.on('click', function () {
            console.log('Button clicked!');
            // Add your logic here
        });
    }
});
