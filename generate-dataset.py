import os
import os
import random
import json
from math import atan2, degrees
from TurtleGraphics import (
    TurtleGraphics,
    Position,
)  # Ensure this matches the module name where TurtleGraphics is defined


def generate_random_movements(tg, num_moves=10):
    center_x = tg.width // 2
    center_y = tg.height // 2
    std_dev = 5  # Standard deviation for the normal distribution

    start_x = random.gauss(center_x, std_dev)
    start_y = random.gauss(center_y, std_dev)
    tg.current_position = Position(start_x, start_y)

    shapes = ["random", "triangle", "square", "circle"]
    shape = random.choice(shapes)

    if shape == "triangle":
        size = random.randint(10, 20)
        for _ in range(3):
            tg.forward(size)
            tg.right(random.randint(70, 110))  # Adding randomness to angles
    elif shape == "square":
        size = random.randint(10, 20)
        for _ in range(4):
            tg.forward(size)
            tg.right(random.randint(80, 100))  # Adding randomness to angles
    elif shape == "circle":
        radius = random.randint(5, 10)
        extent = random.randint(180, 360)  # Partial or full circle
        steps = random.randint(10, 50)
        tg.circle(radius, extent, steps)
    else:  # Random lines
        for _ in range(num_moves):
            distance = random.randint(10, 50)
            tg.forward(distance)
            angle = random.gauss(0, 30)  # Small random angles
            if random.choice([True, False]):
                tg.right(angle)
            else:
                tg.left(angle)

    tg.pen_up()


# Function to generate dataset
def generate_dataset(num_samples=100, output_dir="dataset"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Create subdirectories for images and gcode
    images_dir = os.path.join(output_dir, "images")
    gcode_dir = os.path.join(output_dir, "gcode")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(gcode_dir, exist_ok=True)

    metadata = []

    for i in range(num_samples):
        tg = TurtleGraphics(width=64, height=64, feed_rate=1200)
        tg.pen_down()
        generate_random_movements(tg)

        # Save G-code
        gcode_filename = f"sample_{i:04d}.txt"
        gcode_path = os.path.join(gcode_dir, gcode_filename)
        with open(gcode_path, "w") as gcode_file:
            gcode = tg.export_gcode(scale=0.1)
            gcode_file.write(gcode)

        # Save image
        image_filename = f"sample_{i:04d}.png"
        image_path = os.path.join(images_dir, image_filename)
        tg.save_image(image_path, target_width=64, target_height=64)

        # Add metadata entry
        metadata.append(
            {
                "file_name": os.path.join("images", image_filename),
                "text": os.path.join("gcode", gcode_filename),
            }
        )

        print(f"Saved sample {i:04d}")

    # Save metadata file
    metadata_path = os.path.join(output_dir, "metadata.jsonl")
    with open(metadata_path, "w") as metadata_file:
        for entry in metadata:
            json.dump(entry, metadata_file)
            metadata_file.write("\n")

    print(f"Metadata saved to {metadata_path}")


# Generate the dataset
generate_dataset(num_samples=100, output_dir="dataset")
