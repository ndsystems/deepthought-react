import matplotlib.pyplot as plt
import mpld3
from flask import Flask
from controller import AcquisitionControl

app = Flask(__name__)


@app.route('/')
def index():
    scope = AcquisitionControl("localhost", 2500)
    img = scope.image()
    fig, ax = plt.subplots()
    ax.imshow(img)
    html = mpld3.fig_to_html(fig)
    return html


if __name__ == "__main__":
    app.run()
