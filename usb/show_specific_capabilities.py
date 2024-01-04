from evdev import InputDevice


DEVICE_PATH = '/dev/input/event0'


if __name__ == '__main__':
    gamepad = InputDevice(DEVICE_PATH)
    print(gamepad)

    gamepad.capabilities(verbose=True)
