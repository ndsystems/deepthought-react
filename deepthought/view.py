import matplotlib.pyplot as plt
import mpld3
from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from controller import AcquisitionControl

app = Flask(__name__)
socketio = SocketIO(app)

scope = AcquisitionControl("localhost", 2500)


@app.route('/')
def index():
    img = scope.image()
    html = image_to_html(img)
    return render_template("index.html", mpl_figure=html)


def image_to_html(img):
    fig, ax = plt.subplots()
    ax.imshow(img, origin='lower', interpolation='nearest')
    html = mpld3.fig_to_html(fig)
    return html


@socketio.on('connect')
def hello():
    print("hello world")


@socketio.on('stage')
def stage_update(data):
    print(data)
    emit("updateState", data)


if __name__ == "__main__":
    socketio.run(app)
