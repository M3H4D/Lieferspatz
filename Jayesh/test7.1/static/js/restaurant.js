const socket = io();
const userId = user.RestaurantID; 
socket.emit('join', { role: 'restaurant', id: userId });

socket.on('new_request', (data) => {
    console.log('New request received:', data); // Check if this is logged
    const request = data.request;
    const customerId = data.customer_id;

    showModal(`New Request: ${request}\nAccept?`, (response) => {
        const responseText = response ? "Accepted" : "Declined";
        socket.emit('restaurant_response', {
            customer_id: customerId,
            response: responseText
        });
    });
});

function showModal(message, callback) {
    const modal = document.getElementById('customModal');
    const modalText = document.getElementById('modalText');
    const acceptBtn = document.getElementById('acceptBtn');
    const declineBtn = document.getElementById('declineBtn');

    modalText.textContent = message;
    modal.style.display = "block";

    acceptBtn.onclick = () => {
        modal.style.display = "none";
        callback(true);
    };

    declineBtn.onclick = () => {
        modal.style.display = "none";
        callback(false);
    };
}