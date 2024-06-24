from TurtleGraphics import TurtleGraphics

test_turtle = TurtleGraphics(width=24, height=24, feed_rate=1000)
test_turtle.pen_down()
test_turtle.goto(5, 5)
test_turtle.set_relative_mode()
test_turtle.goto(10, 0)
test_turtle.goto(0, -10)
test_turtle.goto(-10, 0)
test_turtle.goto(-10, -10)
test_turtle.pen_up()
test_turtle.set_absolute_mode()
test_turtle.goto(0, 0)
# test_turtle.goto(24, 24)

instructions = test_turtle.write_gcode(24, 24)
print(instructions)

test_turtle.save_png("./data/gcode-render.png", target_width=24, target_height=24)
