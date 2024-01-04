import evdev

device = evdev.InputDevice('/dev/input/event1')
print(device)

device.capabilities(verbose=True)
