import matplotlib.pyplot as plt
import mpld3
from matplotlib_scalebar.scalebar import ScaleBar


def imshow(image, size=(5, 5), dpi=150):
    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    scalebar = ScaleBar(0.2)
    plt.set_cmap('gray')
    ax.imshow(image, origin='lower', aspect='equal')
    ax.add_artist(scalebar)
    return fig


def imshow_js(image):
    fig = imshow(image)
    js_data = mpld3.fig_to_dict(fig)
    plt.close()
    return js_data
