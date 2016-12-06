from flask import Flask, render_template, json
from flask import url_for
from flask_socketio import SocketIO, send, emit
import json

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


@socketio.on('dearclient')
def send_packet():

    packet = build_dearclient()

    print("sent: " + json.dumps(packet))

    socketio.emit("response", packet, json=True)

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

                # """
                # IMU:
                # +x is front of bot
                # +y is right of bot
                # +z is above bot
                # +pitch is rotating up
                # +roll is barrel roll right
                # +yaw is turning right
                # """

                # """
                # Pressure:
                # pressure is in bars
                # temperature is in Celcius
                # """

                # """
                # THRUSTERS:
                # Each thruster's data is specified here
                # Mapping:
                #     t0
                #     t1
                #     t2
                #     t3
                #     t4
                #     t5
                #     t6
                #     t7
                # Power is -100 to 100
                # """

    packet = json.loads("""
        {   \"Sensors\" : {
                \"IMU\" : {
                    \"x\" : """ + str(imu.x) + """,
                    \"y\" : """ + str(imu.y) + """,
                    \"z\" : """ + str(imu.z) + """,
                    \"pitch\" : """ + str(imu.pitch) + """,
                    \"roll\" : """ + str(imu.roll) + """,
                    \"yaw\" : """ + str(imu.yaw) + """
                },

                \"PRESSURE\" : {
                    \"pressure\" : """ + str(pressure.pressure) + """,
                    \"temperature\" : """ + str(pressure.temperature) + """
                }
            },

            \"Thrusters\" : {
                \"t0\" : { \"power\" : """ + str(thrusters.t1.power) + """ },
                \"t1\" : { \"power\" : """ + str(thrusters.t1.power) + """ },
                \"t2\" : { \"power\" : """ + str(thrusters.t1.power) + """ },
                \"t3\" : { \"power\" : """ + str(thrusters.t1.power) + """ },
                \"t4\" : { \"power\" : """ + str(thrusters.t1.power) + """ },
                \"t5\" : { \"power\" : """ + str(thrusters.t1.power) + """ },
                \"t6\" : { \"power\" : """ + str(thrusters.t1.power) + """ },
                \"t7\" : { \"power\" : """ + str(thrusters.t1.power) + """ }
            }
        }""")

    return packet



# INIT:


if __name__ == '__main__':
    socketio.run(app, debug=True)

