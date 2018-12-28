import matplotlib.pyplot as plt
import MMCorePy


def load_microscope(mmc):
    mmc.loadDevice("Olympus IX83", "OlympusIX83", "Olympus IX83")
    mmc.loadDevice("Objective", "OlympusIX83", "Objective")
    mmc.loadDevice("Light Path", "OlympusIX83", "Light Path")
    mmc.loadDevice("Condenser turret", "OlympusIX83", "Condenser turret")
    mmc.loadDevice("Polarizer", "OlympusIX83", "Polarizer")
    mmc.loadDevice("Dichroic 1", "OlympusIX83", "Dichroic 1")
    mmc.loadDevice("EpiShutter 1", "OlympusIX83", "EpiShutter 1")
    mmc.loadDevice("DiaShutter", "OlympusIX83", "DiaShutter")
    mmc.loadDevice("TransmittedIllumination 1",
                   "OlympusIX83", "TransmittedIllumination 1")
    mmc.loadDevice("TransmittedIllumination 2",
                   "OlympusIX83", "TransmittedIllumination 2")
    mmc.loadDevice("Transmitted Aperture",
                   "OlympusIX83", "Transmitted Aperture")
    mmc.loadDevice("FocusDrive", "OlympusIX83", "FocusDrive")
    mmc.loadDevice("XYStage", "OlympusIX83", "XYStage")
    mmc.loadDevice("Autofocus", "OlympusIX83", "Autofocus")
    mmc.loadDevice("AutofocusDrive", "OlympusIX83", "AutofocusDrive")
    return mmc


def load_camera(mmc):
    mmc.loadDevice("Andor_cam1", "AndorSDK3", "Andor sCMOS Camera")
    mmc.setCameraDevice('Andor_cam1')
    return mmc


def snap_image(exposure_time=200, shutter="epi"):
    shutter_control(shutter, 0)
    mmc.setProperty("Andor_cam1", "Exposure", exposure_time)
    mmc.snapImage()
    shutter_control(shutter, 1)
    return mmc.getImage()


def shutter_control(shutter, state):
    if shutter is "epi":
        mmc.setProperty("EpiShutter 1", "State", state)

    if shutter is "dia":
        mmc.setProperty("DiaShutter", "State", state)
    return


def view_image(img):
    plt.imshow(img, cmap=plt.cm.gray)
    plt.show()


if __name__ == "__main__":
    mmc = MMCorePy.CMMCore()

    mmc = load_microscope(mmc)
    mmc = load_camera(mmc)
    mmc.initializeAllDevices()

    img = snap_image(200, "epi")

    view_image(img)
