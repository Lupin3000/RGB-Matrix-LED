import evdev


if __name__ == '__main__':
    print('Search and listing for devices')
    devices = [evdev.InputDevice(path) for path in evdev.list_devices()]

    for device in devices:
        print(f'Path: {device.path} Name: {device.name} Phys: {device.phys}')
