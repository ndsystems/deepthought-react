import matplotlib.pyplot as plt


def dd(image):
    plt.imshow(image, cmap="gray", clim=[100, 4095])
    plt.show()
    plt.close()
