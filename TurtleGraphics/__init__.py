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
        self.current_position = Position(
            width // 2, height // 2
        )  # Initialize at center
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
        # img = self.image.resize((target_width, target_height), Image.NEAREST)
        img = self.image
        img.save(filename, "png")

    def clear(self):
        self.gcode_moves = []
        self.image = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.draw_obj = ImageDraw.Draw(self.image)


# Example of how to use the TurtleGraphics class
tg = TurtleGraphics(height=64, width=64, feed_rate=1200)
tg.pen_down()
tg.forward(20)
tg.right(90)
tg.forward(20)
tg.right(90)
tg.forward(20)
tg.right(90)
tg.forward(20)
tg.pen_up()

# Export G-code
gcode = tg.export_gcode(scale=0.1)
print("Generated G-code:\n", gcode)

# Save the drawing as PNG
filename = "data/square_64.png"
tg.save_image(filename, target_width=64, target_height=64)
print(f"Image saved to {filename}")
