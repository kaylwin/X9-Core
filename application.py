from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import threading
import os

from rov.rov import ROV

"""
PRIMARY FLASK APPLICATION:

This file handles the primary functions of the webapp. Handles:
    Routing
    SocketIO
        Error Handling
    Flask Init
"""

# GLOBALS:
app = Flask(__name__, static_url_path="", static_folder="frontend")
socketio = SocketIO(app, async_mode=None)

rov = ROV()
tmp_stus = "{IMU: {x: 3, y: 3, z: 3, pitch: 3, roll: 2, yaw: 2}, Pressure: {pressure: 2319, temperature: 0}, Thrusters: {t0: { power: 0}, t1: { power: 0}, t2: { power: 0}, t3: { power: 0}, t4: { power: 0}, t5: { power: 0}, t6: { power: 0}, t7: { power: 0} } }"

# ROUTING:
@app.route('/')
def index():
    print "Send index.html"
    return app.send_static_file('index.html')

@app.route('/UI/')
def index_front():
    print "Send /src/index2.html"
    return app.send_static_file('src/index2.html')

@app.route('/UI/fonts/<path:path>')
def send_font_files(path):
    print "front file"
    print path
    return send_from_directory('frontend/src/', path)

@app.route('/UI/gp/<path:path>')
def send_UI_files(path):
    print os.path.dirname(os.path.realpath(__file__))
    return send_from_directory('frontend/gamepad/', path)

@app.route('/UI/pg2/<path:path>')
def send_index2_page_files(path):
    return app.send_static_file('src/'+path)

# SOCKET-IO:
@socketio.on('dearflask')
def recieve_controls(data):
    # parse json controls object into onside object.
    # print("controls: " + str(json))
    # print('received message: ' + str(data))
    send_packet()

    
@socketio.on('connect')
def on_connect():
    print("CLIENT CONNECTED!")


@socketio.on('disconnect')
def on_disconnect():
    print("CLIENT DISCONNECTED!")


"""
# Error Handling (We should probably do something with this at some point..)
@socketio.on_error()
def error_handler(e):
    print(e)
    print("ERROR CAUGHT BY HANDLER!\n")
"""

# HELPER METHODS:


def send_packet():

    packet = build_dearclient()

    #print "Sent:"
    #print packet

    socketio.emit("dearclient", packet, json=True)


def build_dearclient():
    #return rov.data
    return tmp_stus


if __name__ == '__main__':
    rov_run = threading.Thread(target=rov.run)
    rov_run.daemon = True
    rov_run.start()

    socketio.run(app, debug=True, host="0.0.0.0")
