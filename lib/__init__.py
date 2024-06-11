import tkinter
import turtle_gcode as turtle_gcode
import turtle as turtle_canvas
from PIL import Image


class GcodeRenderImage:
    def __init__(self, canvas_x: int = 28, canvas_y: int = 28):
        self.canvas_x = canvas_x
        self.canvas_y = canvas_y

        # set the drawing canvas
        # create two canvases, one to generate the image another for the drawing
        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(
            self.root, bg="white", height=canvas_y, width=canvas_x
        )
        self.canvas.pack(side=tkinter.LEFT)
        screen = turtle_canvas.TurtleScreen(self.canvas)
        screen.setworldcoordinates(0, 300, 400, 0)
        self.turtle_canvas = turtle_canvas.RawTurtle(screen)
        self.turtle_canvas.speed(0)

        # cache the gcode turtle as well
        self.turtle_gcode = turtle_gcode

        # start with the pen up and go to origin
        self.turtle_canvas.up()
        self.turtle_canvas.goto(0, 0)

        self.turtle_gcode.up()
        self.turtle_gcode.goto(0, 0)

    def pen_down(self):
        self.turtle_canvas.pendown()
        self.turtle_gcode.pendown()

    def pen_up(self):
        self.turtle_canvas.penup()
        self.turtle_gcode.penup()

    def goto(self, x: int, y: int):
        if x is None or y is None:
            raise ValueError("goto needs an x and y coordinate")

        self.turtle_canvas.goto(x, y)
        self.turtle_gcode.goto(x, y)

    def absolute(self):
        pass

    def relative(self):
        pass

    def get_gcode(self):

        penup_command = "G0 Z10"
        pendown_command = "G0 Z0"

        instructions = turtle_gcode.write_gcode(
            self.canvas_x,
            self.canvas_y,
            0,
            0,
            False,
            "centre",
            penup_command,
            pendown_command,
        )
        return instructions

    def write_image(self, filename: str):
        if filename is None:
            raise ValueError("filename not provided")

        self.canvas.postscript(file=filename + ".eps")
        # use PIL to convert to PNG
        img = Image.open(filename + ".eps")
        img.save(filename + ".png", "png")

        self.root.mainloop()
        self.turtle_canvas.screen.mainloop()


## Gimoire chat generated code

import turtle
from dataclasses import dataclass
from PIL import Image
import math


@dataclass
class Position:
    x: float
    y: float
    z: float = 0.0  # Default Z value


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

    def write_gcode(self, info: ScaleInfo) -> str:
        return f"G1 X{info.offset.x + self.end.x * info.scale:.3f} Y{info.offset.y + self.end.y * info.scale:.3f} Z{self.end.z:.3f}"


@dataclass
class CircleMove:
    start: Position
    end: Position
    centre: Position
    radius: float
    extent: float
    steps: float | None

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
                self.start.z,
            )
            gcode += f"G1 X{info.offset.x + new_pos.x * info.scale:.3f} Y{info.offset.y + new_pos.y * info.scale:.3f} Z{new_pos.z:.3f}\n"

        return gcode.strip()

    def _write_gcode_circle_radius(self, info: ScaleInfo) -> str:
        return f"G2 X{info.offset.x + self.end.x * info.scale:.3f} Y{info.offset.y + self.end.y * info.scale:.3f} Z{self.end.z:.3f} R{self.radius * info.scale:.3f}"


class TurtleGraphics:
    def __init__(self, width=800, height=600):
        self.screen = turtle.Screen()
        self.screen.setup(width, height)
        self.turtle = turtle.Turtle()
        self.gcode_moves = []
        self.pen_is_down = True
        self.relative_mode = False

    def set_absolute_mode(self):
        self.relative_mode = False

    def set_relative_mode(self):
        self.relative_mode = True

    def _get_current_position(self):
        return Position(
            self.turtle.xcor(), self.turtle.ycor(), 1.0 if self.pen_is_down else 0.0
        )

    def forward(self, distance):
        start = self._get_current_position()
        self.turtle.forward(distance)
        end = self._get_current_position()
        self.gcode_moves.append(LinearMove(start, end))

    def backward(self, distance):
        start = self._get_current_position()
        self.turtle.backward(distance)
        end = self._get_current_position()
        self.gcode_moves.append(LinearMove(start, end))

    def right(self, angle):
        self.turtle.right(angle)

    def left(self, angle):
        self.turtle.left(angle)

    def goto(self, x, y=None):
        if self.relative_mode:
            start = self._get_current_position()
            self.turtle.goto(start.x + x, start.y + (y if y is not None else 0))
        else:
            start = self._get_current_position()
            self.turtle.goto(x, y)
        end = self._get_current_position()
        self.gcode_moves.append(LinearMove(start, end))

    def circle(self, radius, extent=None, steps=None):
        start = self._get_current_position()
        self.turtle.circle(radius, extent, steps)
        end = self._get_current_position()
        centre = Position(
            start.x - radius * math.cos(math.radians(self.turtle.heading())),
            start.y - radius * math.sin(math.radians(self.turtle.heading())),
            start.z,
        )
        self.gcode_moves.append(CircleMove(start, end, centre, radius, extent, steps))

    def pen_up(self):
        self.pen_is_down = False

    def pen_down(self):
        self.pen_is_down = True

    def write_gcode(
        self,
        width,
        height,
        x=0,
        y=0,
        allow_rotation=False,
        circle_mode="centre",
        penup_command=None,
        pendown_command=None,
    ):
        scale_info = ScaleInfo(
            scale=1.0, do_rotation=False, offset=Position(x, y), top=height, bottom=0
        )
        gcode = []
        for move in self.gcode_moves:
            gcode.append(move.write_gcode(scale_info))
        return "\n".join(gcode)

    def save_png(self, filename):
        canvas = self.screen.getcanvas()
        canvas.postscript(file="temp.ps")
        img = Image.open("temp.ps")
        img.save(filename, "png")

    def clear(self):
        self.turtle.clear()
        self.gcode_moves = []


if __name__ == "__main__":
    tg = TurtleGraphics()
    tg.set_absolute_mode()
    tg.pen_down()
    tg.forward(100)
    tg.right(90)
    tg.forward(100)
    tg.set_relative_mode()
    tg.pen_up()
    tg.left(90)
    tg.forward(50)
    tg.pen_down()
    tg.circle(50)
    print(tg.write_gcode(200, 200))
    tg.save_png("drawing.png")
