from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send
from handler import AcquisitionControl
from viz import imshow_js

app = Flask(__name__)
socketio = SocketIO(app)
scope = AcquisitionControl("localhost", 2500)


@app.route('/')
def index():
    return render_template("index.html")


@socketio.on('image')
def image_to_json(params):
    img = scope.image()
    js_data = imshow_js(img)
    emit("image", js_data)


@socketio.on('get_props')
def get_props():
    emit("get_props", scope.get_all_properties())


if __name__ == "__main__":
    try:
        socketio.run(app, host="0.0.0.0")
    except ValueError:
        pass
