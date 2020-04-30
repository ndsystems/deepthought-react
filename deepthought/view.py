import matplotlib.pyplot as plt
import mpld3
from flask import Flask, render_template, request
from controller import AcquisitionControl

app = Flask(__name__)

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

if __name__ == "__main__":
    app.run()
