from lib import GcodeRenderImage, TurtleGraphics

test_turtle = TurtleGraphics()
# test_turtle.pen_down()
test_turtle.goto(0.1, 0.1)
# test_turtle.pen_up()

instructions = test_turtle.write_gcode(24, 24)
print(instructions)

test_turtle.save_png("./data/gcode-render.png")
