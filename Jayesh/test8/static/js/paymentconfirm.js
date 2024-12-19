const socket = io();

// Join customer-specific room
socket.emit('join_room', { room: `customer_${customerID}` });

// Handle payment submission
document.querySelector('form').addEventListener('submit', function (e) {
    e.preventDefault();
    const notes = document.querySelector('input[name="notestoadd"]').value;
    
    // Emit payment event
    socket.emit('send_payment', { message: `Payment sent with notes: ${notes}` });
    alert("Payment sent. Waiting for restaurant response...");
});

// Receive restaurant acknowledgment
socket.on('restaurant_ack', function (data) {
    alert(`Restaurant Response: ${data.message}`);
});