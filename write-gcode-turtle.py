from TurtleGraphics import TurtleGraphics, Position

# Initialize the TurtleGraphics instance
test_turtle = TurtleGraphics(width=800, height=800, feed_rate=1000)
test_turtle.set_absolute_mode()

# Start at the center position
test_turtle.current_position = Position(test_turtle.width // 2, test_turtle.height // 2)
test_turtle.current_angle = 0

# Draw the square
test_turtle.pen_down()
test_turtle.forward(100)
test_turtle.right(90)
test_turtle.forward(100)
test_turtle.right(90)
test_turtle.forward(100)
test_turtle.right(90)
test_turtle.forward(100)
test_turtle.right(90)  # Complete the square
test_turtle.pen_up()

# Generate G-code
instructions = test_turtle.write_gcode(800, 800)
print(instructions)

# Save the drawing as PNG
test_turtle.save_png("square.png", target_width=24, target_height=24)
