from configs import get_default
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from handler import AcquisitionControl
from viz import imshow_js
from pprint import pprint
import json
import time


# connect to the mcu server
default = get_default()
hostname = default["mcu_server"]["hostname"]
port = int(default["mcu_server"]["port"])

scope = AcquisitionControl(hostname, port)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*')


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on("connect")
def connected(*args):
    print("socket connected")


@socketio.on("disconnect")
def disconnected(*args):
    print("socket disconnected")


@socketio.on("camera_props")
def update_camera_props(props):
    print("recv :camera_props")


@socketio.on("snap")
def snap_image():
    img = scope.image()
    js_data = imshow_js(img)
    print("recv: snap")
    emit("image", js_data)


@socketio.on("live")
def start_live_acquisition():
    scope.startContinuousSequenceAcquisition(1)
    while True:
        img = scope.getLastImage()
        if scope.getRemainingImageCount() > 0:
            img = scope.getLastImage()
            emit("image", imshow_js(img))
            print("live emitting")

        else:
            print('No frame')

        time.sleep(0.1)


@socketio.on("stop_snap")
def stop_snap():
    stop[0] = false


def dict_to_string(some_dict):
    return json.dumps(some_dict)


@socketio.on('get_props')
def get_props():
    props = scope.get_all_properties()
    print("recv: get_props")
    emit("recv_device_states", props)


if __name__ == "__main__":
    hostname = default["flask_server"]["hostname"]
    port = int(default["flask_server"]["port"])

    try:
        socketio.run(app, host=hostname, port=port)
    except ValueError:
        pass
