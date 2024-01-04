from evdev import InputDevice, list_devices
from sys import exit


def get_controller_path() -> str:
    """
    Get controller linux path
    :return: actual path as string (or empty string if no controller found)
    """
    input_path = ''

    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if device.name.startswith('Google LLC Stadia Controller'):
            input_path = device.path

    return input_path


device_path = get_controller_path()

if not device_path:
    print('No Google Stadia controller found')
    exit(1)

gamepad = InputDevice(device_path)
