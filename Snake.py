from random import randint
from threading import Thread
from time import sleep

from signal import signal, SIGINT
from evdev import ecodes
from rgbmatrix import RGBMatrix, graphics

from lib.terminate_application import signal_handler
from lib.collision_helper import check_point_point_collision
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
        self._font = graphics.Font()
        self._font.LoadFont("fonts/4x6.bdf")
        self._fontcolor = graphics.Color(150, 150, 150)

    def draw(self, points) -> None:
        """
        Draw interface and points on the canvas
        :param points: integer value
        :return: None
        """
        graphics.DrawText(self._matrix, self._font, 1, 6, self._fontcolor, f'{int(points)}')
        graphics.DrawLine(self._matrix, 0, 7, options.cols - 1, 7, self._fontcolor)


class Fruit:
    def __init__(self, panel, min_x: int, max_x: int, min_y: int, max_y: int):
        """
        Fruit constructor
        :param panel: canvas to display
        :param min_x: minimum x integer value
        :param max_x: maximum x integer value
        :param min_y: minimum y integer value
        :param max_y: maximum y integer value
        """
        self._matrix = panel
        self._min_x = int(min_x)
        self._max_x = int(max_x)
        self._min_y = int(min_y)
        self._max_y = int(max_y)

        self.pos_x = None
        self.pos_y = None

        self.reset()

    def reset(self) -> None:
        """
        Reset fruit x,y position
        :return: None
        """
        self.pos_x = randint(int(self._min_x), int(self._max_x))
        self.pos_y = randint(int(self._min_y), int(self._max_y))

    def draw(self) -> None:
        """
        Draw fruit on the canvas
        :return: None
        """
        self._matrix.SetPixel(self.pos_x, self.pos_y, 250, 250, 0)


class SnakeHead:
    def __init__(self, panel):
        """
        SnakeHead constructor
        :param panel: canvas to display
        """
        self._matrix = panel
        self._speed = 1
        self.pos_x = int(options.cols // 2)
        self.pos_y = int(options.rows // 2)
        self.direction = None

    def _move(self) -> None:
        """
        Move the snake in different directions
        :return: None
        """
        if self.direction == "up":
            self.pos_y -= self._speed

        if self.direction == "down":
            self.pos_y += self._speed

        if self.direction == "left":
            self.pos_x -= self._speed

        if self.direction == "right":
            self.pos_x += self._speed

    def draw(self) -> None:
        """
        Draw snake on canvas
        :return: None
        """
        self._move()
        self._matrix.SetPixel(self.pos_x, self.pos_y, 0, 0, 255)


class SnakeSegment:
    def __init__(self, panel, x: int, y: int):
        """
        SnakeSegment constructor
        :param panel: canvas to display
        :param x: integer value for the x position
        :param y: integer value for the y position
        """
        self._matrix = panel
        self.pos_x = int(x)
        self.pos_y = int(y)

    def draw(self) -> None:
        """
        Draw snake on canvas
        :return: None
        """
        self._matrix.SetPixel(self.pos_x, self.pos_y, 0, 100, 255)


def handle_input(controller, target) -> None:
    """
    Handle user controller input
    :param controller: controller object
    :param target: target object to set direction for move
    :return: None
    """
    for event in controller.read_loop():
        if event.type == ecodes.EV_ABS:
            if event.code == ecodes.ABS_X:
                if event.value > 245:
                    target.direction = 'right'
                if event.value < 10:
                    target.direction = 'left'

            if event.code == ecodes.ABS_Y:
                if event.value > 245:
                    target.direction = 'down'
                if event.value < 10:
                    target.direction = 'up'


if __name__ == '__main__':
    signal(SIGINT, signal_handler)

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    score = 0
    collision = False

    interface = Interface(panel=canvas)
    fruit = Fruit(panel=canvas, min_x=0, max_x=int(options.cols - 1), min_y=8, max_y=int(options.rows - 1))
    snake = SnakeHead(panel=canvas)
    snake_tail_segments = []

    input_thread = Thread(target=handle_input, args=(gamepad, snake, ), daemon=True)
    input_thread.start()

    while True:
        matrix.Clear()

        if collision:
            break

        if check_point_point_collision(point_a=[snake.pos_x, snake.pos_y], point_b=[fruit.pos_x, fruit.pos_y]):
            segment = SnakeSegment(panel=canvas, x=snake.pos_x, y=snake.pos_y)
            snake_tail_segments.append(segment)
            score += 1
            fruit.reset()

        fruit.draw()

        for index in range(len(snake_tail_segments) - 1, 0, - 1):
            snake_tail_segments[index].pos_x = snake_tail_segments[index - 1].pos_x
            snake_tail_segments[index].pos_y = snake_tail_segments[index - 1].pos_y

        if len(snake_tail_segments) > 0:
            snake_tail_segments[0].pos_x = snake.pos_x
            snake_tail_segments[0].pos_y = snake.pos_y

        for item in snake_tail_segments:
            item.draw()

        snake.draw()

        for item in snake_tail_segments:
            if snake.pos_x == item.pos_x and snake.pos_y == item.pos_y:
                collision = True

        if not -1 < snake.pos_x < options.cols or not 8 < snake.pos_y < options.rows:
            collision = True

        interface.draw(score)

        matrix.SwapOnVSync(canvas)
        sleep(DELAY_IN_SECONDS)
