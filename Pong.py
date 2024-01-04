from random import random
from threading import Thread
from time import sleep

from signal import signal, SIGINT
from evdev import ecodes
from rgbmatrix import RGBMatrix, graphics

from lib.terminate_application import signal_handler
from lib.collision_helper import check_circle_line_collision
from lib.matrix_configuration import options
from lib.stadia_controller import gamepad


DELAY_IN_SECONDS = .075


class Interface:
    def __init__(self, panel):
        """
        Interface constructor
        :param panel: canvas to display
        """
        self._matrix = panel
        self._color = graphics.Color(200, 200, 200)

    def draw(self) -> None:
        """
        Draw the game on display
        :return: None
        """
        graphics.DrawLine(self._matrix, 0, 0, 63, 0, self._color)
        graphics.DrawLine(self._matrix, 0, 31, 63, 31, self._color)
        graphics.DrawLine(self._matrix, 63, 0, 63, 31, self._color)


class Paddle:
    def __init__(self, panel):
        """
        Paddle constructor
        :param panel: canvas to display
        """
        self._matrix = panel
        self._color = graphics.Color(200, 200, 200)
        self.pos_x = 1
        self.pos_y = 16
        self.height = 6
        self.speed = 2

    def draw(self) -> None:
        """
        Draw the game paddle on display
        :return: None
        """
        graphics.DrawLine(self._matrix,
                          self.pos_x,
                          self.pos_y - (self.height // 2),
                          self.pos_x,
                          self.pos_y + (self.height // 2),
                          self._color)

        graphics.DrawLine(self._matrix,
                          self.pos_x - 1,
                          self.pos_y - (self.height // 2),
                          self.pos_x - 1,
                          self.pos_y + (self.height // 2),
                          self._color)


class Ball:
    def __init__(self, panel):
        """
        Ball constructor
        :param panel: canvas to display
        """
        self._matrix = panel
        self._color = graphics.Color(10, 10, 200)
        self._reset_ball()

        self.radius = 2

    @staticmethod
    def generate_random_number() -> int:
        """
        Generate random number -2 or 2
        :return: value as integer
        """
        random_number = 2 if random() < 0.5 else -2

        return random_number

    def _reset_ball(self) -> None:
        """
        Reset ball x,y position
        :return: None
        """
        self.pos_x = int(options.cols // 2 + 10)
        self.pos_y = int(options.rows // 2)
        self.speed_x = Ball.generate_random_number()
        self.speed_y = Ball.generate_random_number()

    def _move(self) -> None:
        """
        Move the ball
        :return: None
        """
        global lives

        self.pos_x += self.speed_x
        self.pos_y += self.speed_y

        if self.pos_x <= 0:
            lives -= 1
            flicker()
            self._reset_ball()

        if not self.pos_x <= 60:
            self.speed_x *= -1

        if not 4 <= self.pos_y <= 28:
            self.speed_y *= -1

    def draw(self) -> None:
        """
        Draw the ball
        :return: None
        """
        self._move()

        graphics.DrawCircle(self._matrix, self.pos_x, self.pos_y, self.radius, self._color)
        graphics.DrawLine(self._matrix, self.pos_x - 1, self.pos_y - 1, self.pos_x + 1, self.pos_y - 1, self._color)
        graphics.DrawLine(self._matrix, self.pos_x - 1, self.pos_y, self.pos_x + 1, self.pos_y, self._color)
        graphics.DrawLine(self._matrix, self.pos_x - 1, self.pos_y + 1, self.pos_x + 1, self.pos_y + 1, self._color)


def handle_input(controller, target) -> None:
    """
    Handle user controller input
    :param controller: controller object
    :param target: target object to move
    :return: None
    """
    abs_v = 17

    for event in controller.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == abs_v and event.value == -1 and target.pos_y >= 5:
                target.pos_y -= target.speed

            if event.code == abs_v and event.value == 1 and target.pos_y <= 26:
                target.pos_y += target.speed


def flicker() -> None:
    """
    Flicker function for display
    :return: None
    """
    global matrix
    global canvas
    global lives

    if lives > 0:
        text = 'Next chance'
    elif lives == 0:
        text = 'You will die'
    else:
        text = 'You lost all'

    for _ in range(3):
        matrix.Fill(0, 0, 0)
        sleep(.15)
        matrix.Fill(200, 0, 0)
        graphics.DrawText(canvas, font, 10, 20, fontColor, text)
        sleep(.15)


if __name__ == "__main__":
    signal(SIGINT, signal_handler)

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()
    font = graphics.Font()
    font.LoadFont("fonts/4x6.bdf")
    fontColor = graphics.Color(255, 255, 0)

    lives = 5
    interface = Interface(panel=canvas)
    paddle = Paddle(panel=canvas)
    ball = Ball(panel=canvas)

    input_thread = Thread(target=handle_input, args=(gamepad, paddle,), daemon=True)
    input_thread.start()

    while True:
        matrix.Clear()

        if lives <= 0:
            break

        ball.draw()
        interface.draw()
        paddle.draw()

        circle_list = [ball.pos_x, ball.pos_y, ball.radius]
        line_list = [paddle.pos_x,
                     paddle.pos_y - (paddle.height // 2),
                     paddle.pos_x,
                     paddle.pos_y + (paddle.height // 2)]

        if check_circle_line_collision(circle=circle_list, line=line_list):
            ball.speed_x *= -1

        matrix.SwapOnVSync(canvas)
        sleep(DELAY_IN_SECONDS)
