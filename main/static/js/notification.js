export function connectWebSocket(id_) {
    const socket = new WebSocket('ws://localhost:12345');

    socket.addEventListener('open', event => {
        console.log('WebSocket is open now.');
        socket.send(id_)

    });

    socket.addEventListener('message', event => {
        console.log('Message from server:', event.data);
        const messagesDiv = document.getElementById('ouput');
        messagesDiv.textContent = event.data;
    });

    socket.addEventListener('close', event => {
        console.log("WebSocket is closed now.");
        const submitButton = document.getElementById('submit')
        submitButton.disabled = false
    });
}

function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        let r = Math.random() * 16 | 0;  // Generate a random number between 0 and 15
        let v = (c === 'x') ? r : (r & 0x3 | 0x8); // Randomly select the digit for y (8, 9, A, or B)
        return v.toString(16); // Convert to hexadecimal
    });
}