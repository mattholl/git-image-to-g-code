from dataclasses import dataclass
from PIL import Image, ImageDraw
import math


@dataclass
class Position:
    x: float
    y: float


@dataclass
class LinearMove:
    start: Position
    end: Position
    feed_rate: int

    def write_gcode(self, scale: float) -> str:
        return (
            f"G1 X{self.end.x * scale:.3f} Y{self.end.y * scale:.3f} F{self.feed_rate}"
        )

    def draw(self, draw_obj):
        draw_obj.line(
            [self.start.x, self.start.y, self.end.x, self.end.y], fill=(0, 0, 0)
        )


class TurtleGraphics:
    def __init__(self, width=800, height=600, feed_rate=1500):
        self.gcode_moves = []
        self.pen_is_down = True
        self.feed_rate = feed_rate
        self.width = width
        self.height = height

        # Create a PIL image and draw object
        self.image = Image.new("RGB", (width, height), (255, 255, 255))
        self.draw_obj = ImageDraw.Draw(self.image)
        self.current_position = Position(0, 0)  # Initialize at top left
        self.current_angle = 0  # Initialize angle

    def _get_current_position(self):
        return self.current_position

    def forward(self, distance):
        start = self._get_current_position()
        angle = math.radians(self.current_angle)
        end = Position(
            start.x + distance * math.cos(angle), start.y - distance * math.sin(angle)
        )
        if self.pen_is_down:
            self.gcode_moves.append(LinearMove(start, end, self.feed_rate))
            LinearMove(start, end, self.feed_rate).draw(self.draw_obj)
        self.current_position = end

    def backward(self, distance):
        self.forward(-distance)

    def right(self, angle):
        self.current_angle -= angle

    def left(self, angle):
        self.current_angle += angle

    def circle(self, radius, extent=None, steps=None):
        start = self._get_current_position()
        angle = math.radians(self.current_angle + 90)
        centre = Position(
            start.x + radius * math.cos(angle), start.y + radius * math.sin(angle)
        )
        if extent is None:
            extent = 360
        if steps is None:
            steps = 36  # Default steps for a full circle
        step_angle = extent / steps
        for _ in range(steps):
            angle += math.radians(step_angle)
            end = Position(
                centre.x + radius * math.cos(angle), centre.y + radius * math.sin(angle)
            )
            if self.pen_is_down:
                self.gcode_moves.append(LinearMove(start, end, self.feed_rate))
                LinearMove(start, end, self.feed_rate).draw(self.draw_obj)
            start = end

    def pen_up(self):
        self.pen_is_down = False

    def pen_down(self):
        self.pen_is_down = True

    def export_gcode(self, scale=1.0):
        gcode = ["G21 ; Set units to millimeters", "G90 ; Absolute positioning"]
        for move in self.gcode_moves:
            gcode.append(move.write_gcode(scale))
        return "\n".join(gcode)

    def save_image(self, filename, target_width=64, target_height=64):
        img = self.image.resize((target_width, target_height), Image.NEAREST)
        reflected_img = img.transpose(Image.FLIP_TOP_BOTTOM)
        reflected_img.save(filename, "png")

    def clear(self):
        self.gcode_moves = []
        self.image = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.draw_obj = ImageDraw.Draw(self.image)
