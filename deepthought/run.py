import hardware
from view import dd

if __name__ == "__main__":
    scope = hardware.Microscope("configs\Bright_Star.cfg")
    scope.load()
    scope.channel("BF")

