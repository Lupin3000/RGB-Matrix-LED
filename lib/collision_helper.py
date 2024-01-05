from math import sqrt


def check_circle_line_collision(circle: list, line: list) -> bool:
    """
    Check if circle is colliding with line
    :param circle: list of circle values (x, y, radius)
    :param line: list of line values (x1, y1, x2, y2)
    :return: bool
    """
    cx, cy, cr = circle
    x1, y1, x2, y2 = line

    closest_x = max(x1, min(cx, x2))
    closest_y = max(y1, min(cy, y2))
    distance = sqrt((cx - closest_x) ** 2 + (cy - closest_y) ** 2)

    return distance <= cr


def check_point_point_collision(point_a: list, point_b: list) -> bool:
    """
    Check if two points are on same x, y coordinates
    :param point_a: list of points (x, y)
    :param point_b: list of points (x, y)
    :return: bool
    """
    x1, y1 = point_a
    x2, y2 = point_b

    if x1 == x2 and y1 == y2:
        return True
    else:
        return False


def check_point_rectangle_collision(point: list, rectangle: list) -> bool:
    """
    Check if a point is inside a rectangle
    :param point: list of point coordinates (x, y)
    :param rectangle: list of rectangle coordinates (x, y, width, height)
    """
    x_point, y_point = point
    x_rect, y_rect, width, height = rectangle

    return (x_rect <= x_point <= x_rect + width) and (y_rect <= y_point <= y_rect + height)
