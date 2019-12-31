import MMCorePy
import os


mm2_path = "C:\Program Files\Micro-Manager-2.0gamma"


def load(config_path):
    config_abspath = os.path.abspath(config_path)
    os.chdir(mm2_path)
    mmc = MMCorePy.CMMCore()
    mmc.loadSystemConfiguration(config_abspath)

    return mmc
