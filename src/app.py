from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO
import json
import os

app = Flask(__name__)
socketio = SocketIO(app)

# Load prayers from JSON
def load_prayers():
    with open('src/data/prayers.json', 'r') as file:
        return json.load(file)

# Save prayers to JSON
def save_prayers(prayers):
    with open('src/data/prayers.json', 'w') as file:
        json.dump(prayers, file, indent=4)

@app.route('/')
def index():
    prayers = load_prayers()
    return render_template('index.html', prayers=prayers)

@app.route('/increment_counter', methods=['POST'])
def increment_counter():
    data = request.json
    prayer_id = data['id']
    prayers = load_prayers()

    for prayer in prayers:
        if prayer['id'] == prayer_id:
            prayer['counter'] += 1
            break

    save_prayers(prayers)
    socketio.emit('update_counter', {'id': prayer_id, 'counter': prayer['counter']})
    return jsonify(success=True)

@app.route('/add_prayer_request', methods=['POST'])
def add_prayer_request():
    data = request.json
    new_request = {"id": len(load_prayers()) + 1, "text": data['text'], "counter": 0, "prayed": False}
    prayers = load_prayers()
    prayers.append(new_request)
    save_prayers(prayers)
    socketio.emit('new_prayer', new_request)
    return jsonify(success=True)

if __name__ == '__main__':
    socketio.run(app)
