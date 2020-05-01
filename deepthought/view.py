import matplotlib.pyplot as plt
import mpld3
import json
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from controller import AcquisitionControl
import time

app = Flask(__name__)
socketio = SocketIO(app)

scope = AcquisitionControl("localhost", 2500)


@app.route('/')
def index():
    return render_template("index.html")

@socketio.on('image')
def image_to_json(params):
    img = scope.image()

    fig, ax = plt.subplots(dpi=150)
    ax.imshow(img, origin='lower', interpolation='nearest')
    ax.set_axis_off()

    js_data = mpld3.fig_to_dict(fig)
    emit("image", js_data)
    time.sleep(0.5)


@socketio.on('connect')
def hello():
    print("hello world")



@socketio.on('stage')
def stage_update(data):
    print(data)
    emit("updateState", data)

#https://stackoverflow.com/questions/25069898/display-mpld3-chart-in-html-with-django
if __name__ == "__main__":
    socketio.run(app)
