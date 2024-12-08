const socket = io();
const userId = user.RestaurantID; 
socket.emit('join', { role: 'restaurant', id: userId });

socket.on('new_request', (data) => {
    console.log('New request received:', data); // Check if this is logged
    const request = data.request;
    const customerId = data.customer_id;

    const response = confirm(`New Request: ${request}\nAccept?`);
    const responseText = response ? "Accepted" : "Declined";

    socket.emit('restaurant_response', {
        customer_id: customerId,
        response: responseText
    });
});
