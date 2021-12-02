from time import sleep

from openrazer.client import DeviceManager


class Effect:
    def __init__(self):
        device_manager = DeviceManager()

        print("Found {} Razer devices".format(len(device_manager.devices)))

        self.devices = device_manager.devices
        for device in self.devices:
            if not device.fx.advanced:
                print("Skipping device " + device.name + " (" + device.serial + ")")
                self.devices.remove(device)

        # Disable daemon effect syncing.
        # Without this, the daemon will try to set the lighting effect to every device.
        device_manager.sync_effects = False

    def restore(self):
        for device in self.devices:
            device.fx.advanced.restore()

    def paint(self):
        raise NotImplementedError()

    def play(self, fps):
        try:
            while True:
                self.paint()
                sleep(1.0 / fps)
        finally:
            self.restore()
