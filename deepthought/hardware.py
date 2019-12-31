import MMCorePy
import os


mm2_path = "C:\Program Files\Micro-Manager-2.0gamma"


def load(config_file_path):
    os.chdir(mm2_path)
    config_file_abspath = os.path.abspath(config_file_path)

    mmc = MMCorePy.CMMCore()
    mmc.loadSystemConfiguration(config_path)

    return mmc
