document.addEventListener('DOMContentLoaded', function () {
    // Add 'change' event listener to file input
    var fileInput = document.getElementById('document');
    fileInput.addEventListener('change', function (event) {
        console.log('File input has changed. Processing file...');
        var file = fileInput.files[0];
        if (file) {
            // Extract filename and file extension
            var filename = file.name;
            var fileExtension = filename.split('.').pop();

            // Set the hidden inputs with the extracted values
            document.getElementsByName('filename')[0].value = filename;
            document.getElementsByName('fileextension')[0].value = fileExtension;

            // Read the content of the file and encode as hexadecimal
            var reader = new FileReader();
            reader.onload = function (e) {
                var fileContentArray = new Uint8Array(e.target.result);
                var fileContentHex = Array.from(fileContentArray, byte => byte.toString(16).padStart(2, '0')).join('');
                document.getElementsByName('document')[0].value = fileContentHex;
                console.log('File content populated.');
            };
            reader.readAsArrayBuffer(file);
        } else {
            console.log('No file selected.');
        }
    });

    // Function to toggle file input based on folder flag checkbox
    function toggleFileInput() {
        console.log('Toggling file input...');
        var folderFlagCheckbox = document.querySelector('input[name="folderflag"]');
        var fileInputContainer = document.getElementById('fileInputContainer');
        var fileInput = document.getElementById('document');

        if (folderFlagCheckbox.checked) {
            // If folderflag is checked, hide the file input
            console.log('Folder flag is checked. Hiding file input.');
            fileInputContainer.style.display = 'none';

            // Remove the required attribute for the file input
            fileInput.removeAttribute('required');

            // Set the hidden inputs to empty when folderflag is checked
            document.getElementsByName('filename')[0].value = '';
            document.getElementsByName('fileextension')[0].value = '';
            document.getElementsByName('document')[0].value = '';  // Ensure it's an empty string
        } else {
            // If folderflag is unchecked, show the file input
            console.log('Folder flag is unchecked. Showing file input.');
            fileInputContainer.style.display = 'block';

            // Set the required attribute for the file input
            fileInput.setAttribute('required', 'required');
        }
    }

    // Add 'input' event listener to documentnode input
    var documentNodeInput = document.getElementById('documentnode');
    documentNodeInput.addEventListener('input', function (event) {
        var userInput = documentNodeInput.value.trim();

        // Check if the server-side variable is defined
        var existingNodes = {% if existing_document_nodes is defined %}JSON.parse('{{ existing_document_nodes | tojson | safe }}'){% else %}[]{% endif %};
        console.log('Existing Nodes:', existingNodes);
        // Check if the entered documentnode already exists
        if (existingNodes.includes(userInput)) {
            alert('Existing document node cannot be added. Please choose a different document node.');
            // Clear the input field or ask the user to change the input
            documentNodeInput.value = '';
        }
    });

    // Handle the server response after submitting the form
    var form = document.getElementById('add-doc');
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting normally

        // Perform additional client-side validations if needed

        // Submit the form using AJAX
        fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
        })
        .then(response => {
            if (response.ok) {
                // Success, handle the successful response (e.g., redirect or display a success message)
                alert('Document added successfully!');
                // You might want to redirect the user to a different page or update the UI accordingly
            } else if (response.status === 400) {
                // Handle the case where the document node already exists
                return response.json();
            } else {
                // Handle other error cases
                throw new Error('Unexpected error occurred');
            }
        })
        .then(data => {
            // Display an error message to the user
            alert('Error: ' + data.error);
        })
        .catch(error => {
            console.error('Error:', error.message);
        });
    });
});
