const socket = io();

// Join restaurant-specific room
socket.emit('join_room', { room: `restaurant_${restaurantID}` });

// Handle incoming payment notifications
socket.on('payment_received', function (data) {
    const customerId = data.customer_id;
    const message = data.message;
    const response = confirm(`Payment received from customer ${customerId}: ${message}. Accept payment?`);

    if (response) {
        socket.emit('restaurant_reply', { customer_id: customerId, message: 'Payment accepted' });
    } else {
        socket.emit('restaurant_reply', { customer_id: customerId, message: 'Payment declined' });
    }
});