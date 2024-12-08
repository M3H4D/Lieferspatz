const socket = io();
const userId = user.CustomerID; 
socket.emit('join', { role: 'customer', id: userId });

function sendRequest() {
    const restaurantId = document.getElementById('restaurant_id').value;
    const requestDetails = document.getElementById('request_details').value;

    socket.emit('customer_request', {
        customer_id: userId,
        restaurant_id: restaurantId,
        request: requestDetails
    });
    alert("Request sent!");
}

socket.on('acknowledgment', (data) => {
    alert(`Response from Restaurant: ${data.response}`);
});
