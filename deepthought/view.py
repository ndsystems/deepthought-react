import matplotlib.pyplot as plt
import mpld3
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from handler import AcquisitionControl
import time


app = Flask(__name__)
socketio = SocketIO(app)


scope = AcquisitionControl("localhost", 2500)


@app.route('/')
def index():
    return render_template("index.html")


def make_image(image, size=(5, 5), dpi=150):
    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.set_cmap('gray')
    ax.imshow(image, aspect='equal')
    return fig


@socketio.on('image')
def image_to_json(params):
    img = scope.image()

    fig, ax = plt.subplots(dpi=150)
    ax.imshow(img, cmap="gray", origin='lower', interpolation='nearest')
    ax.set_axis_off()

    js_data = mpld3.fig_to_dict(fig)

    plt.close()
    emit("image", js_data)
    time.sleep(0.1)


@socketio.on('connect')
def hello():
    print("hello world")


@socketio.on('stage')
def stage_update(data):
    print(data)
    emit("updateState", data)


if __name__ == "__main__":
    try:
        socketio.run(app, host="0.0.0.0")
    except ValueError:
        pass
