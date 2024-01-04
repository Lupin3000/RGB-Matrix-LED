from evdev import InputDevice, list_devices


DEVICE_PATH = '/dev/input/event0'


if __name__ == '__main__':
    print('Search and listing for devices')
    devices = [InputDevice(path) for path in list_devices()]

    for device in devices:
        print(f'Path: {device.path} Name: {device.name} Phys: {device.phys}')
