from flask import Flask, send_from_directory
from flask_socketio import SocketIO
import threading
import os

from rov.rov import ROV

packet = {
    IMU: {
        x: 7,
        y: 6,
        z: 5,
        pitch: 4,
        roll: 3,
        yaw: 2
    },
    PRESSURE: {
        pressure: 9,
        temperature: 72
    },
    Thrusters: {
        t0 : { power: "11"},
        t1 : { power: "14"},
        t2 : { power: "23"},
        t3 : { power: "7"},
        t4 : { power: "15"},
        t5 : { power: "4"},
        t6 : { power: "18"},
        t7 : { power: "10"}
    }
}

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
#    print "UI file"
#    print path
    print os.path.dirname(os.path.realpath(__file__))
    return send_from_directory('frontend/gamepad/', path)

@app.route('/UI/pg2/<path:path>')
def send_index2_page_files(path):
    print "Page file"
    print path
    return app.send_static_file('src/'+path)

# SOCKET-IO:
@socketio.on('dearflask')
def recieve_controls(data):
    # parse json controls object into onside object.
    # print("controls: " + str(json))
    print('received message: ' + str(data))


@socketio.on('dearclient')
def send_packet():

    packet = build_dearclient()

    #print "Sent:"
    #print packet

    socketio.emit("dearflask", packet, json=True)


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


def build_dearclient():

    return rov.data


if __name__ == '__main__':
    rov_run = threading.Thread(target=rov.run)
    rov_run.daemon = True
    rov_run.start()

    socketio.run(app, debug=True, host="0.0.0.0")
