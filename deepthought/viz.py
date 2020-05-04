import matplotlib.pyplot as plt
import mpld3


def imshow(image, size=(5, 5), dpi=150):
    fig = plt.figure()
    fig.set_size_inches(size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    fig.add_axes(ax)
    plt.set_cmap('gray')
    ax.imshow(image, aspect='equal')
    return fig


def imshow_js(image):
    fig = imshow(image)
    js_data = mpld3.fig_to_dict(fig)
    plt.close()
    return js_data
