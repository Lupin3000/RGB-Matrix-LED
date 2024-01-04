from rgbmatrix import RGBMatrixOptions, RGBMatrix, graphics
from evdev import InputDevice, list_devices, ecodes
from threading import Thread
from time import sleep


options = RGBMatrixOptions()
options.chain_length = 1
options.cols = 64
options.rows = 32
options.parallel = 1
options.brightness = 50
options.disable_hardware_pulsing = True
options.drop_privileges = 1
options.gpio_slowdown = 1
options.hardware_mapping = 'adafruit-hat'
options.inverse_colors = False
options.led_rgb_sequence = "RGB"
options.multiplexing = 0
options.pixel_mapper_config = ''
options.pwm_bits = 11
options.pwm_dither_bits = 0
options.pwm_lsb_nanoseconds = 130
options.row_address_type = 0
options.scan_mode = 0
options.show_refresh_rate = False


class Point:
    def __init__(self, panel):
        self.x, self.y = 32, 16
        self.matrix = panel
        self._color = graphics.Color(200, 200, 200)

    def draw(self, screen):
        self.matrix.SetPixel(self.x, self.y, 255, 0, 0)
        graphics.DrawCircle(screen, self.x, self.y, 1, self._color)


def get_controller_path() -> str:
    device_path = '/dev/input/event0'

    devices = [InputDevice(path) for path in list_devices()]
    for device in devices:
        if device.name.startswith('Google LLC Stadia Controller'):
            device_path = device.path

    return device_path


def handle_input() -> None:
    global gamepad

    for event in gamepad.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code in [ecodes.ABS_X, ecodes.ABS_Y]:
                if event.value > 245:
                    pressed_states[event.code] = 1
                elif event.value < 10:
                    pressed_states[event.code] = -1
                else:
                    pressed_states[event.code] = 0


def update_point_position():
    global point

    while True:
        # Update the point's position based on the pressed states
        if pressed_states[ecodes.ABS_X] == 1 and point.x < 63:
            point.x += 1
        elif pressed_states[ecodes.ABS_X] == -1 and point.x > 0:
            point.x -= 1

        if pressed_states[ecodes.ABS_Y] == 1 and point.y < 31:
            point.y += 1
        elif pressed_states[ecodes.ABS_Y] == -1 and point.y > 0:
            point.y -= 1

        sleep(0.05)


if __name__ == "__main__":
    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    point = Point(matrix)

    gamepad = InputDevice(get_controller_path())
    pressed_states = {ecodes.ABS_X: 0, ecodes.ABS_Y: 0}

    input_thread = Thread(target=handle_input, daemon=True)
    input_thread.start()

    update_thread = Thread(target=update_point_position, daemon=True)
    update_thread.start()

    while True:
        matrix.Clear()

        point.draw(screen=canvas)

        matrix.SwapOnVSync(canvas)
        sleep(0.075)
