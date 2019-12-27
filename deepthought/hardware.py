import MMCorePy
import os

mm2_path = ["C:", "Program Files", "Micro-Manager-2.0gamma"]
mm2_path = os.path.join(*mm2_path)


class Microscope():
    def __init__(self, config_path):
        self.user_dir = os.getcwd()

    def load(self):
        config_path = os.path.abspath(config_path)
        self.mmc = MMCorePy.CMMCore()
        os.chdir(mm2_path)  # cwd to mm2 path for dlls to load
        self.mmc.loadSystemConfiguration(config_path)

    def unload(self):
        return


if __name__ == "__main__":
    scope = Microscope(os.path.join(*["config", "Bright_Star.cfg"])
    scope.load()
    # ...
    scope.unload()
