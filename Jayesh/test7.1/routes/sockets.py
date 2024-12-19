from flask_socketio import SocketIO, emit, join_room, leave_room

socketio = SocketIO()

@socketio.on('join')
def handle_join(data):
    role = data['role']
    user_id = data['id']
    room = f"{role}_{user_id}"
    join_room(room)
    print(f"{role.capitalize()} with ID {user_id} joined room {room}")

@socketio.on('customer_request')
def handle_customer_request(data):
    restaurant_id = data['restaurant_id']
    request = data['request']

    room = f"restaurant_{restaurant_id}"
    emit('new_request', {'request': request, 'customer_id': data['customer_id']}, room=room)

@socketio.on('restaurant_response')
def handle_restaurant_response(data):
    customer_id = data['customer_id']
    response = data['response']

    room = f"customer_{customer_id}"
    emit('acknowledgment', {'response': response}, room=room)
