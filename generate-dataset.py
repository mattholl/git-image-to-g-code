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

    # Create subdirectories for train, validation, and test sets
    for split in ["train", "validation", "test"]:
        os.makedirs(os.path.join(output_dir, split), exist_ok=True)

    metadata = {split: [] for split in ["train", "validation", "test"]}

    for i in range(num_samples):
        tg = TurtleGraphics(width=64, height=64, feed_rate=1200)
        tg.pen_down()
        generate_random_movements(tg)

        # Determine which split this sample belongs to
        if i < int(0.7 * num_samples):
            split = "train"
        elif i < int(0.85 * num_samples):
            split = "validation"
        else:
            split = "test"

        # Save G-code
        gcode_filename = f"gcode_{i:04d}.txt"
        gcode_path = os.path.join(output_dir, split, gcode_filename)
        with open(gcode_path, "w") as gcode_file:
            gcode = tg.export_gcode(scale=0.1)
            gcode_file.write(gcode)

        # Save image
        image_filename = f"image_{i:04d}.png"
        image_path = os.path.join(output_dir, split, image_filename)
        tg.save_image(image_path, target_width=64, target_height=64)

        # Add metadata entry
        metadata[split].append({"file_name": image_filename, "text": gcode_filename})

        print(f"Saved sample {i:04d} to {split} set")

    # Save metadata files for each split
    for split, split_metadata in metadata.items():
        metadata_path = os.path.join(output_dir, split, "metadata.jsonl")
        with open(metadata_path, "w") as metadata_file:
            for entry in split_metadata:
                json.dump(entry, metadata_file)
                metadata_file.write("\n")
        print(f"{split.capitalize()} metadata saved to {metadata_path}")


# Generate the dataset
generate_dataset(num_samples=10, output_dir="dataset")
