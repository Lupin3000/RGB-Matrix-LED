from evdev import InputDevice, list_devices, categorize, ecodes

gamepad = InputDevice(list_devices()[0])
print(gamepad)

for event in gamepad.read_loop():
    print(categorize(event))
    print(f'Type: {event.type}')
    print(f'Code: {event.code}')
    print(f'Value: {event.value}')
