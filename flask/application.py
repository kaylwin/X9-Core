from flask import Flask, render_template, json
from flask import url_for
from flask_socketio import SocketIO, send, emit
from json import JSONEncoder

from python.pressure import Pressure
from python.imu import IMU
from python.thrusters import Thrusters

#
# PRIMARY FLASK APPLICATION:
#
# This file handles the primary functions of the webapp. Handles:
#   Routing
#   SocketIO
#       Error Handling
#   Flask Init


# GLOBALS:
async_mode = None
app = Flask(__name__, static_folder="static")
socketio = SocketIO(app, async_mode=async_mode)
thrusters = Thrusters()
imu = IMU()
thrusters = Thrusters()
pressure = Pressure()


# Statistics:
recieve_count = 0  # keeps count of how many json objects flask has recieved.
send_count = 0  # keeps count of how many json objects flask has sent.


# ROUTING:

@app.route('/')
def index():
    return render_template('index.html')

# SOCKET-IO:


@socketio.on('dearflask')
def recieve_controls(json):
    # parse json controls object into onside object.
    # print("controls: " + str(json))
    global recieve_count
    recieve_count += 1
    print(recieve_count)
    print('received message: ' + str(json))


@socketio.on('dearflask')
def send_packet():

    packet = {

        "controls": {
            "absolutecontrols" : {
                "x" : 1,
                "y" : 1,
                "z" : 1,
                "roll" : 1,
                "pitch" : 1,
                "yaw" : 1
            },
            "controls" : {
                "buttons" : {
                    "a": 1,
                    "b": 1,
                    "x": 1,
                    "y": 1,
                    "z": 1,
                    "lb": 1,
                    "rb": 1,
                    "lt": 1,
                    "rt": 1,
                    "slct": 1,
                    "strt": 1,
                    "lpress": 1,
                    "rpress": 1,
                    "up": 1,
                    "down": 1,
                    "left": 1,
                    "right": 1
                },
                "axes": {
                    "left": {
                        "x": 0,
                        "y": 1
                    },
                    "right": {
                        "x": 2,
                        "y": 3
                    }

                }
            }

        }
    }


    print("sent: " + json.dumps(packet))

    socketio.emit("dearclient", packet, json=True)

    global send_count
    send_count += 1


@socketio.on('connect')
def on_connect():
    print("CLIENT CONNECTED!")


@socketio.on('disconnect')
def on_disconnect():
    print("CLIENT DISCONNECTED!")

# Error Handling


@socketio.on_error()
def error_handler(e):
    print(e);
    print("ERROR CAUGHT BY HANDLER!\n")

# HELPER METHODS:


def build_dearclient():

    # TODO:
    # Once this has been certified to work, the dictionary will be
    # created only once and then updated with new values in this method.

                """
                IMU:
                +x is front of bot
                +y is right of bot
                +z is above bot
                +pitch is rotating up
                +roll is barrel roll right
                +yaw is turning right
                """




# INIT:


if __name__ == '__main__':
    socketio.run(app, debug=True)

