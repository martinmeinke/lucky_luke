import hid
from enum import Enum

RAW_EPSIZE = 64


class ColorMode(Enum):
    COLOR_MODE_DEFAULT = 0
    COLOR_MODE_FADEOUT = 1
    COLOR_MODE_ROLLING = 2


def pad_message(payload):
    return payload + b"\x00" * (RAW_EPSIZE - len(payload))


def tobyte(data):
    if type(data) is bytes:
        return data
    else:
        return (data).to_bytes(1, "big")


def tobytes(data):
    out = b""
    for num in data:
        out += tobyte(num)
    return out


class Moonlander:
    device = None

    def __init__(self):

        # moonlander
        vendor_id = int.from_bytes(b"\x04\x83", "big")
        product_id = int.from_bytes(b"\xdf\x11", "big")
        vendor_id = int.from_bytes(b"\x32\x97", "big")
        product_id = int.from_bytes(b"\x19\x69", "big")
        usage_page = int.from_bytes(b"\xFF\x60", "big")
        usage_id = int.from_bytes(b"\x61", "big")

        for device in hid.enumerate():
            print(
                f"{device['vendor_id']=} {device['product_id']=} {device['usage_page']=} {device['usage']=}"
            )
            if (
                device["vendor_id"] == vendor_id
                and device["product_id"] == product_id
                and device["usage_page"] == usage_page
                and device["usage"] == usage_id
            ):
                self.device = hid.Device(path=device["path"])
                break
        if self.device is None:
            print("Unable to identify device!")
            exit(1)

    def close(self):
        self.device.close()

    def send(self, data):
        self.device.write(pad_message(data))

    def led_rgb(self, index, r, g, b):
        data = tobytes([2, 0, index, r, g, b])
        self.send(data)

    def color_mode(self, color_mode: ColorMode):
        data = tobytes([3, color_mode.value])
        self.send(data)

    def clear_all(self):
        data = tobytes([1, 0])
        self.send(data)
