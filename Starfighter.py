from time import sleep
from threading import Thread
from signal import signal, SIGINT

from evdev import ecodes
from rgbmatrix import RGBMatrix, graphics

from lib.terminate_application import signal_handler
from lib.matrix_configuration import options
from lib.stadia_controller import gamepad
from lib.collision_helper import check_point_rectangle_collision


DELAY_IN_SECONDS = 0.075


class Fighter:

    FIGHTER_SPEED = 1
    BULLET_SPEED = 2

    def __init__(self, panel):
        """
        Fighter constructor
        :param panel: canvas to display
        """
        self._matrix = panel
        self._icon = [
            [2, 1, 1, 1, 0],
            [0, 1, 1, 0, 0],
            [2, 1, 1, 1, 1],
            [0, 1, 1, 0, 0],
            [2, 1, 1, 1, 0]
        ]
        self._shield_color = graphics.Color(200, 200, 200)

        self.width = len(self._icon[0])
        self.height = len(self._icon)
        self.pos_x = 1
        self.pos_y = int(options.rows // 2 - self.height // 2)

        self.shield = 10

        self.bullet_state = False
        self.bullet_x = 0
        self.bullet_y = 0

    def draw(self) -> None:
        """
        Draw the fighter on canvas
        :return: None
        """
        for y, row in enumerate(self._icon):
            for x, c in enumerate(row):
                if c == 1:
                    self._matrix.SetPixel(x + self.pos_x, y + self.pos_y, 100, 100, 100)
                if c == 2:
                    self._matrix.SetPixel(x + self.pos_x, y + self.pos_y, 200, 0, 0)

        graphics.DrawLine(self._matrix, 1, 0, self.shield, 0, self._shield_color)


class Enemy:

    BULLET_SPEED = 3

    def __init__(self, panel):
        """
        Enemy constructor
        :param panel: canvas to display
        """
        self._matrix = panel
        self._icon = [
            [0, 0, 0, 1, 2],
            [0, 0, 1, 1, 2],
            [1, 1, 1, 1, 0],
            [0, 0, 1, 1, 2],
            [0, 0, 0, 1, 2]
        ]
        self._speed = 1
        self._shield_color = graphics.Color(200, 200, 200)

        self.width = len(self._icon[0])
        self.height = len(self._icon)
        self.pos_x = int(options.cols - self.width) - 1
        self.pos_y = int(options.rows // 2 - self.height // 2)

        self.shield = 10

        self.bullet_state = False
        self.bullet_x = 0
        self.bullet_y = 0

    def _move(self) -> tuple:
        """
        Change y position and speed of the enemy
        :return: tuple
        """
        self.pos_y += self._speed

        if self.pos_y <= 2:
            self._speed *= -1

        if self.pos_y >= int(options.rows - self.height):
            self._speed *= -1

        x = self.pos_x
        y = self.pos_y

        return x, y

    def draw(self) -> None:
        """
        Draw the enemy on canvas
        :return: None
        """
        x1, y2 = self._move()

        for y, row in enumerate(self._icon):
            for x, c in enumerate(row):
                if c == 1:
                    self._matrix.SetPixel(x + x1, y + y2, 100, 100, 100)
                if c == 2:
                    self._matrix.SetPixel(x + x1, y + y2, 200, 0, 0)

        start_x = int(options.cols - 2)
        end_x = int(options.cols - 2 - self.shield)
        graphics.DrawLine(self._matrix, start_x, 0, end_x, 0, self._shield_color)


def handle_input(controller, target) -> None:
    """
    Handle user controller input
    :param controller: controller object
    :param target: target object for trigger shoot
    :return: None
    """
    global pressed_states

    btn_a = 304

    for event in controller.read_loop():
        if event.type == ecodes.EV_KEY and event.value == 1:
            if event.code == btn_a:
                if not target.bullet_state:
                    target.bullet_state = True
                    target.bullet_x = int(target.width)
                    target.bullet_y = int(target.pos_y + target.height // 2)

        if event.type == ecodes.EV_ABS:
            if event.code in [ecodes.ABS_X, ecodes.ABS_Y]:
                if event.value > 245:
                    pressed_states[event.code] = 1
                elif event.value < 10:
                    pressed_states[event.code] = -1
                else:
                    pressed_states[event.code] = 0


def update_target_position(target) -> None:
    """
    Updates the target position on specific state
    :param target: the target to update y position
    :return: None
    """
    while True:
        if pressed_states[ecodes.ABS_Y] == 1 and target.pos_y < int(options.rows - target.height):
            target.pos_y += target.FIGHTER_SPEED
        elif pressed_states[ecodes.ABS_Y] == -1 and target.pos_y > 2:
            target.pos_y -= target.FIGHTER_SPEED

        sleep(0.05)


if __name__ == '__main__':
    signal(SIGINT, signal_handler)

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    fighter = Fighter(panel=canvas)
    enemy = Enemy(panel=canvas)

    pressed_states = {ecodes.ABS_X: 0, ecodes.ABS_Y: 0}

    input_thread = Thread(target=handle_input, args=(gamepad, fighter,), daemon=True)
    input_thread.start()

    update_thread = Thread(target=update_target_position, args=(fighter,), daemon=True)
    update_thread.start()

    while True:
        matrix.Clear()

        # game break condition
        if fighter.shield <= 0 or enemy.shield <= 0:
            break

        # game logic
        fighter.draw()

        if fighter.bullet_state and fighter.bullet_x < options.cols:
            canvas.SetPixel(fighter.bullet_x, fighter.bullet_y, 0, 0, 200)
            fighter.bullet_x += fighter.BULLET_SPEED

        if fighter.bullet_x >= int(options.cols):
            fighter.bullet_state = False
            fighter.bullet_x = 0
            fighter.bullet_y = 0

        enemy.draw()

        if not enemy.bullet_state:
            enemy.bullet_x = enemy.pos_x
            enemy.bullet_y = int(enemy.pos_y + enemy.height // 2)
            enemy.bullet_state = True

        if enemy.bullet_state and enemy.bullet_x >= 0:
            enemy.bullet_x -= enemy.BULLET_SPEED
            canvas.SetPixel(enemy.bullet_x, enemy.bullet_y, 0, 200, 0)

        if enemy.bullet_state and enemy.bullet_x <= 0:
            enemy.bullet_state = False

        fighter_point = [fighter.bullet_x, fighter.bullet_y]
        enemy_point = [enemy.bullet_x, enemy.bullet_y]
        fighter_rectangle = [fighter.pos_x, fighter.pos_y, fighter.width, fighter.height]
        enemy_rectangle = [enemy.pos_x, enemy.pos_y, enemy.width, enemy.height]

        if check_point_rectangle_collision(point=fighter_point, rectangle=enemy_rectangle):
            fighter.bullet_state = False
            fighter.bullet_x = 0
            fighter.bullet_y = 0
            enemy.shield -= 1

        if check_point_rectangle_collision(point=enemy_point, rectangle=fighter_rectangle):
            enemy.bullet_state = False
            enemy.bullet_x = 0
            enemy.bullet_y = 0
            fighter.shield -= 1

        # sync matrix canvas
        matrix.SwapOnVSync(canvas)
        sleep(DELAY_IN_SECONDS)
