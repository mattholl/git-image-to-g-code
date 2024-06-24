# import tkinter
# import turtle_gcode as turtle_gcode
# import turtle as turtle_canvas
# from PIL import Image


# class GcodeRenderImage:
#     def __init__(self, canvas_x: int = 28, canvas_y: int = 28):
#         self.canvas_x = canvas_x
#         self.canvas_y = canvas_y

#         # set the drawing canvas
#         # create two canvases, one to generate the image another for the drawing
#         self.root = tkinter.Tk()
#         self.canvas = tkinter.Canvas(
#             self.root, bg="white", height=canvas_y, width=canvas_x
#         )
#         self.canvas.pack(side=tkinter.LEFT)
#         screen = turtle_canvas.TurtleScreen(self.canvas)
#         screen.setworldcoordinates(0, 300, 400, 0)
#         self.turtle_canvas = turtle_canvas.RawTurtle(screen)
#         self.turtle_canvas.speed(0)

#         # cache the gcode turtle as well
#         self.turtle_gcode = turtle_gcode

#         # start with the pen up and go to origin
#         self.turtle_canvas.up()
#         self.turtle_canvas.goto(0, 0)

#         self.turtle_gcode.up()
#         self.turtle_gcode.goto(0, 0)

#     def pen_down(self):
#         self.turtle_canvas.pendown()
#         self.turtle_gcode.pendown()

#     def pen_up(self):
#         self.turtle_canvas.penup()
#         self.turtle_gcode.penup()

#     def goto(self, x: int, y: int):
#         if x is None or y is None:
#             raise ValueError("goto needs an x and y coordinate")

#         self.turtle_canvas.goto(x, y)
#         self.turtle_gcode.goto(x, y)

#     def absolute(self):
#         pass

#     def relative(self):
#         pass

#     def get_gcode(self):

#         penup_command = "G0 Z10"
#         pendown_command = "G0 Z0"

#         instructions = turtle_gcode.write_gcode(
#             self.canvas_x,
#             self.canvas_y,
#             0,
#             0,
#             False,
#             "centre",
#             penup_command,
#             pendown_command,
#         )
#         return instructions

#     def write_image(self, filename: str):
#         if filename is None:
#             raise ValueError("filename not provided")

#         self.canvas.postscript(file=filename + ".eps")
#         # use PIL to convert to PNG
#         img = Image.open(filename + ".eps")
#         img.save(filename + ".png", "png")

#         self.root.mainloop()
#         self.turtle_canvas.screen.mainloop()


## Gimoire chat generated code
import turtle
from dataclasses import dataclass
from PIL import Image, ImageOps, ImageDraw
import math


@dataclass
class Position:
    x: float
    y: float


@dataclass
class ScaleInfo:
    scale: float
    do_rotation: bool
    offset: Position
    top: float
    bottom: float


@dataclass
class LinearMove:
    start: Position
    end: Position
    feed_rate: int

    def write_gcode(self, info: ScaleInfo) -> str:
        return f"G1 X{info.offset.x + self.end.x * info.scale:.3f} Y{info.offset.y + self.end.y * info.scale:.3f} F{self.feed_rate}"

    def draw(self, draw_obj):
        draw_obj.line(
            [self.start.x, self.start.y, self.end.x, self.end.y], fill=(0, 0, 0)
        )


@dataclass
class CircleMove:
    start: Position
    end: Position
    centre: Position
    radius: float
    extent: float
    steps: float | None
    feed_rate: int

    def write_gcode(self, info: ScaleInfo) -> str:
        if self.steps is None:
            return self._write_gcode_circle_radius(info)
        else:
            return self._write_gcode_steps(info)

    def _write_gcode_steps(self, info: ScaleInfo) -> str:
        angle = math.atan2(self.start.y - self.centre.y, self.start.x - self.centre.x)
        step_size = self.extent / self.steps
        if self.radius < 0:
            step_size = -step_size

        gcode = ""
        for _ in range(self.steps):
            angle += step_size
            new_pos = Position(
                self.centre.x + self.radius * math.cos(angle),
                self.centre.y + self.radius * math.sin(angle),
            )
            gcode += f"G1 X{info.offset.x + new_pos.x * info.scale:.3f} Y{info.offset.y + new_pos.y * info.scale:.3f} F{self.feed_rate}\n"

        return gcode.strip()

    def _write_gcode_circle_radius(self, info: ScaleInfo) -> str:
        return f"G2 X{info.offset.x + self.end.x * info.scale:.3f} Y{info.offset.y + self.end.y * info.scale:.3f} R{self.radius * info.scale:.3f} F{self.feed_rate}"

    def draw(self, draw_obj):
        bbox = [
            self.centre.x - self.radius,
            self.centre.y - self.radius,
            self.centre.x + self.radius,
            self.centre.y + self.radius,
        ]
        start_angle = math.degrees(
            math.atan2(self.start.y - self.centre.y, self.start.x - self.centre.x)
        )
        if self.extent is None:
            end_angle = start_angle + 360 if self.radius > 0 else start_angle - 360
        else:
            end_angle = (
                start_angle + math.degrees(self.extent)
                if self.radius > 0
                else start_angle - math.degrees(self.extent)
            )
        draw_obj.arc(bbox, start=start_angle, end=end_angle, fill=(0, 0, 0))


class TurtleGraphics:
    def __init__(self, width=800, height=600, feed_rate=1500):
        self.gcode_moves = []
        self.pen_is_down = True
        self.relative_mode = False
        self.feed_rate = feed_rate
        self.width = width
        self.height = height

        # Create a PIL image and draw object
        self.image = Image.new("RGB", (width, height), (255, 255, 255))
        self.draw_obj = ImageDraw.Draw(self.image)

    def set_absolute_mode(self):
        if self.relative_mode:
            self.relative_mode = False
            self.gcode_moves.append("G90")  # Absolute positioning

    def set_relative_mode(self):
        if not self.relative_mode:
            self.relative_mode = True
            self.gcode_moves.append("G91")  # Relative positioning

    def _get_current_position(self):
        return self.current_position

    def forward(self, distance):
        start = self._get_current_position()
        angle = math.radians(self.current_angle)
        end = Position(
            start.x + distance * math.cos(angle), start.y + distance * math.sin(angle)
        )
        self.gcode_moves.append(LinearMove(start, end, self.feed_rate))
        if self.pen_is_down:
            LinearMove(start, end, self.feed_rate).draw(self.draw_obj)
        self.current_position = end

    def backward(self, distance):
        start = self._get_current_position()
        angle = math.radians(self.current_angle)
        end = Position(
            start.x - distance * math.cos(angle), start.y - distance * math.sin(angle)
        )
        self.gcode_moves.append(LinearMove(start, end, self.feed_rate))
        if self.pen_is_down:
            LinearMove(start, end, self.feed_rate).draw(self.draw_obj)
        self.current_position = end

    def right(self, angle):
        self.current_angle -= angle

    def left(self, angle):
        self.current_angle += angle

    def goto(self, x, y=None):
        start = self._get_current_position()
        if self.relative_mode:
            end = Position(start.x + x, start.y + (y if y is not None else 0))
        else:
            end = Position(x, y if y is not None else start.y)
        self.gcode_moves.append(LinearMove(start, end, self.feed_rate))
        if self.pen_is_down:
            LinearMove(start, end, self.feed_rate).draw(self.draw_obj)
        self.current_position = end

    def circle(self, radius, extent=None, steps=None):
        start = self._get_current_position()
        angle = math.radians(self.current_angle + 90)
        centre = Position(
            start.x + radius * math.cos(angle), start.y + radius * math.sin(angle)
        )
        if extent is None:
            extent = 360
        end_angle = self.current_angle + (extent if radius > 0 else -extent)
        end_x = centre.x + radius * math.cos(math.radians(end_angle - 90))
        end_y = centre.y + radius * math.sin(math.radians(end_angle - 90))
        end = Position(end_x, end_y)
        self.gcode_moves.append(
            CircleMove(start, end, centre, radius, extent, steps, self.feed_rate)
        )
        if self.pen_is_down:
            CircleMove(start, end, centre, radius, extent, steps, self.feed_rate).draw(
                self.draw_obj
            )
        self.current_position = end

    def pen_up(self):
        self.pen_is_down = False
        self.gcode_moves.append("G0 Z1.000")

    def pen_down(self):
        self.pen_is_down = True
        self.gcode_moves.append("G0 Z0.000")

    def write_gcode(
        self, width, height, x=0, y=0, allow_rotation=False, circle_mode="centre"
    ):
        scale_info = ScaleInfo(
            scale=1.0, do_rotation=False, offset=Position(x, y), top=height, bottom=0
        )
        gcode = []
        for move in self.gcode_moves:
            if isinstance(move, str):
                gcode.append(move)
            else:
                gcode.append(move.write_gcode(scale_info))
        return "\n".join(gcode)

    def save_png(self, filename, target_width=24, target_height=24):
        # Scale the image for higher quality
        scale_factor = 10
        large_size = (self.width * scale_factor, self.height * scale_factor)
        large_image = self.image.resize(large_size, Image.LANCZOS)

        # Crop to bounding box of non-transparent areas
        bbox = large_image.getbbox()
        large_image = large_image.crop(bbox)

        # Resize to the target dimensions
        img = large_image.resize((target_width, target_height), Image.LANCZOS)
        img.save(filename, "png")

    def clear(self):
        self.gcode_moves = []
        self.image = Image.new("RGB", (self.width, self.height), (255, 255, 255))
        self.draw_obj = ImageDraw.Draw(self.image)


if __name__ == "__main__":
    tg = TurtleGraphics(feed_rate=1200)
    tg.set_absolute_mode()
    tg.pen_down()
    tg.current_position = Position(0, 0)
    tg.current_angle = 0
    tg.forward(100)
    tg.right(90)
