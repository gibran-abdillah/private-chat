from flask import Flask, request, render_template
from flask_socketio import SocketIO, emit, send
import os 

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(10)

LIST_USERS = {}
QUEUE_USERS = []

socketio = SocketIO(app, cors_allowed_origin='*')

def check_queue(username) -> list:
    for id, value in enumerate(QUEUE_USERS):
        if value == username:
            QUEUE_USERS.remove(id)
    return QUEUE_USERS


@app.route('/')
def index_route():
    return render_template('index.html')

@socketio.on('username')
def add_username(username):
    if LIST_USERS.get(username):
        print('username dah ada')
        emit('error_username', username)
    else:
        LIST_USERS[username] = request.sid
        emit('valid_username', username)
    print(LIST_USERS)

@socketio.on('find_partner', namespace='/private')
def find_partner(username):
    if len(QUEUE_USERS) == 0:
        print('QUEUE ADDED ', username)
        QUEUE_USERS.append(LIST_USERS.get(username))
    else:
        print('Udah ada sebelumnya ')
        filtered_queue = check_queue(username).pop()
        print(filtered_queue)
        emit('found_partner', namespace='/private')

if __name__ == '__main__':
    socketio.run(app, debug=True)
