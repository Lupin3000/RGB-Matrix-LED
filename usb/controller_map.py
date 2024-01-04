from evdev import InputDevice, categorize, ecodes

gamepad = InputDevice('/dev/input/event0')

btn_a = 304
btn_b = 305
btn_x = 307
btn_y = 308

abs_h = 16
abs_v = 17

print('Please press the different buttons and sticks')

for event in gamepad.read_loop():

    # key events
    if event.type == ecodes.EV_KEY and event.value == 1:
        if event.code == btn_a:
            print(f'Button A pressed: value {event.value} code {event.code}')

        if event.code == btn_b:
            print(f'Button B pressed: value {event.value} code {event.code}')

        if event.code == btn_x:
            print(f'Button X pressed: value {event.value} code {event.code}')

        if event.code == btn_y:
            print(f'Button Y pressed: value {event.value} code {event.code}')

    # abs events
    if event.type == ecodes.EV_ABS:
        if event.code == abs_v and event.value == -1:
            print(f'Up pressed: value {event.value} code {event.code}')

        if event.code == abs_v and event.value == 1:
            print(f'Down pressed: value {event.value} code {event.code}')

        if event.code == abs_h and event.value == -1:
            print(f"Left pressed: value {event.value} code {event.code}")

        if event.code == abs_h and event.value == 1:
            print(f"Right pressed: value {event.value} code {event.code}")

        #if event.code == ecodes.ABS_X:
        #    print(f'Absolute X pressed: value {event.value} code {event.code}')

        if event.code == ecodes.ABS_Y:
            print(f'Absolute Y pressed: value {event.value} code {event.code}')
