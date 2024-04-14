#!/usr/bin/env python

from hid_rgb import Moonlander, ColorMode
import time
from pynput import keyboard

board = Moonlander()


def on_press(key):
    # Mapping of special keys to their ASCII values or representations
    special_keys = {
        "space": 32,  # Space
        "enter": 13,  # Carriage return
        "tab": 9,  # Horizontal tab
        # Add other special keys you're interested in here
    }

    try:
        if hasattr(key, "char") and key.char is not None:
            # Directly printable ASCII characters
            ascii_val = ord(key.char)
            print(f"Alphanumeric key {key.char} pressed / {ascii_val}")
        else:
            # Attempt to handle special keys by name
            key_name = key.name if hasattr(key, "name") else ""
            ascii_val = special_keys.get(key_name.lower(), None)

            if ascii_val is not None:
                print(f"Special key {key_name} pressed / {ascii_val}")
            else:
                print(f"Other key {key} pressed, no ASCII representation available")

        # Here, add your logic to handle the ascii_val, for example:
        if ascii_val is not None:
            board.led_rgb(ascii_val, 255, 255, 255)

    except AttributeError:
        print(f"Unhandled key {key} pressed")


def on_release(key):
    print(f"Key {key} released")
    # Stop listener
    if key == keyboard.Key.esc:
        return False


if __name__ == "__main__":
    board.clear_all()
    board.color_mode(ColorMode.COLOR_MODE_FADEOUT)
    # Collect events until released
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    msg = "Hallo, 123"

    for c in msg:
        input_int = ord(c)
        board.led_rgb(input_int, 255, 0, 255)
        time.sleep(0.2)
