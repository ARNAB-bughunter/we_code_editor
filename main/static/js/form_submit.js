import { connectWebSocket } from "./notification.js";

// Function to handle form submission by extracting content from the <pre><code> block
async function submitForm(event) {
    event.preventDefault(); // Prevent the default form submission

    const codeBlock = document.getElementById('editableCode');
    const hiddenCodeInput = document.getElementById('hiddenCode');
    const submitButton = document.getElementById('submit')

    submitButton.disabled = true

    // Get the code content from the editable <pre><code> block
    hiddenCodeInput.value = codeBlock.innerText; // Use innerText to get plain text

    // Submit the form using the Fetch API
    const response = await fetch(document.getElementById('jsonForm').action, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ code: hiddenCodeInput.value })
    });




    // Handle the response
    if (response.ok) {
        console.log("OK");
        const jsonResponse = await response.json()
        // console.log(JSON.stringify(jsonResponse))
        connectWebSocket(jsonResponse['id_'])
    } else {
        console.error('Submission failed');
        alert('Failed to submit the code. Please try again.');
    }
}

// Attach the submitForm function to the form's submit event
document.getElementById('jsonForm').addEventListener('submit', submitForm);
