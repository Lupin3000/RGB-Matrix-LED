from evdev import InputDevice, list_devices, categorize, ecodes


DEVICE_PATH = '/dev/input/event0'


if __name__ == '__main__':
    gamepad = InputDevice(DEVICE_PATH)
    print(gamepad)

    print('Press all controller buttons:')
    for event in gamepad.read_loop():
        print(categorize(event))
        print(f'Type: {event.type}')
        print(f'Code: {event.code}')
        print(f'Value: {event.value}')
