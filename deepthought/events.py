"""To keep track of changes to the microscope"""

import pymmcore


class PyMMEventCallBack(pymmcore.MMEventCallback):
    @classmethod
    def onPropertiesChanged():
        print("something changed")

    def onStagePositionChanged(self, *args):
        print("stage position changed ", args)

    def onExposureChanged(self, *args):
        print("exposure changed ", args)
