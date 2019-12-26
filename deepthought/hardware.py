import MMCorePy
import os
current_dir = os.getcwd()
os.chdir("C:\Program Files\Micro-Manager-2.0gamma")


def loadDevices(filepath):
    mmc = MMCorePy.CMMCore()
    mmc.loadSystemConfiguration(current_dir + filepath)
    return mmc


def snap_image(mmc, exposure_time=200, shutter="epi"):
    mmc.setAutoShutter(True)
    mmc.setProperty("Andor_cam1", "Exposure", exposure_time)
    mmc.snapImage()
    return mmc.getImage()


def shutter_control(mmc, shutter, state):
    if shutter is "epi":
        mmc.setProperty("EpiShutter 1", "State", state)

    if shutter is "dia":
        mmc.setProperty("DiaShutter", "State", state)
    return


if __name__ == "__main__":
    mmc = loadDevices()
    mmc.initializeAllDevices()
    img = snap_image(mmc, 200, "epi")
