import matplotlib.pyplot as plt
import mpld3
from flask import Flask, render_template, request
from controller import AcquisitionControl

app = Flask(__name__)
scope = AcquisitionControl("localhost", 2500)

@app.route('/')
def index():
    img = scope.image()
    fig, ax = plt.subplots()
    ax.imshow(img)
    html = mpld3.fig_to_html(fig)
    return render_template("index.html", mpl_figure=html)

@app.route('/', methods=['POST'])
def my_form_post():
    z_value = float(request.form['z_value'])
    scope.setPosition(z_value)
    return '', 204

if __name__ == "__main__":
    app.run()
