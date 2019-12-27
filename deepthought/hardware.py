import MMCorePy
import os

mm2_path = "C:\Program Files\Micro-Manager-2.0gamma"


class Microscope():
    def __init__(self, config_path):
        self.config_path = os.path.abspath(config_path)
        self.user_dir = os.getcwd()

    def load(self):
        self.mmc = MMCorePy.CMMCore()
        # cwd to mm2 path for dlls to load
        os.chdir(mm2_path)
        self.mmc.loadSystemConfiguration(self.config_path)

    def unload(self):
        self.mmc.reset()

    def state(self):
        self.mmc.getSystemState()

    def channel(self, channel):
        self.mmc.setConfig("channel", channel)

    def objective(self, objective):
        self.mmc.setConfig("objective", objective)

    def snap(self, exposure=1):
        self.mmc.setExposure(exposure)
        self.mmc.setCameraDevice("left_port")
        self.mmc.snapImage()
        return self.mmc.getImage()


if __name__ == "__main__":
    pass
