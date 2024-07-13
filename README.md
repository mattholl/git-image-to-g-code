# learning_to_draw_02

## G-Code Generation with AI

G-code instructs 3D printers and 2D plotters using simple "move to" commands with X and Y coordinates in 2D or 3D space.

Inspired by my interest in machine drawing, this project uses the latest open-source AI models to create a Large Language Model (LLM) that generates G-code from images.

The dataset, generated procedurally, includes both images and corresponding G-code. I developed the Python code for this project with the help of ChatGPT for quick suggestions and Claude.ai for debugging and refinement.

This project demonstrates the innovative use of AI in automating G-code generation for creative and practical applications.


### Transformer based gcode instruction generator

#### 1. Create a dataset
small image + gcode instructions to draw it

#### 2. Train vision transformer neural network
- x: image of a line
- y: gcode to draw that line


ChatGPT prompt.

This a multi-modal image to text problem.

Now that we have the dataset we need to define a vision transformer model to be able to the take the image and train to produce the g-code in respone. This shold be useing huggingface as much as possible.

- define transformer neural network and test it on a small dataset.
- use the huggingface ecosystem assuming an API in the environment called HUGGINGFACE_API_KEY
- use the vision transformer model

here you can find a python notebook on how to train a vision transformer model - https://github.com/NielsRogge/Transformers-Tutorials/blob/master/VisionTransformer/Fine_tuning_the_Vision_Transformer_on_CIFAR_10_with_PyTorch_Lightning.ipynb

so in the end I want a hugging face transformer model which will take an image as input and output the gcode which can be used to draw it. An image is used as input mapped to text, with this dataset the training should be straightforward.

3. g-code to png turtle image render

4?. create an image on the blockchain of the drawing as well




### With Claude I reqeusted a modification to the code

     Start new chat

Starred
Star chats you use often
Recents

Generating Image Metadata Files

    Deep Learning Image Classification Pipeline

View all
Free plan
Help & support
M
M

Here is my code for generating images and the g-code to draw them:

import os
import random
from math import atan2, degrees
from TurtleGraphics import (
 TurtleGraphics,
 Position,
) # Ensure this matches the module name where TurtleGraphics is defined
def generate_random_movements(tg, num_moves=10):
 center_x = tg.width // 2
 center_y = tg.height // 2
 std_dev = 5 # Standard deviation for the normal distribution
 start_x = random.gauss(center_x, std_dev)
 start_y = random.gauss(center_y, std_dev)
 tg.current_position = Position(start_x, starty)
 shapes = ["random", "triangle", "square", "circle"]
 shape = random.choice(shapes)
if shape == "triangle":
 size = random.randint(10, 20)
for  in range(3):
 tg.forward(size)
 tg.right(random.randint(70, 110)) # Adding randomness to angles
elif shape == "square":
 size = random.randint(10, 20)
for _ in range(4):
 tg.forward(size)
 tg.right(random.randint(80, 100)) # Adding randomness to angles
elif shape == "circle":
 radius = random.randint(5, 10)
 extent = random.randint(180, 360) # Partial or full circle
 steps = random.randint(10, 50)
 tg.circle(radius, extent, steps)
else: # Random lines
for * in range(num*moves):
 distance = random.randint(10, 50)
 tg.forward(distance)
 angle = random.gauss(0, 30) # Small random angles
if random.choice([True, False]):
 tg.right(angle)
else:
 tg.left(angle)
 tg.pen_up()
# Function to generate dataset
def generate_dataset(num_samples=100, output_dir="dataset"):
if not os.path.exists(output_dir):
 os.makedirs(output_dir)
for i in range(num_samples):
 tg = TurtleGraphics(width=64, height=64, feed_rate=1200)
 tg.pen_down()
generate_random_movements(tg)
# Save G-code
 gcode_filename = os.path.join(outputdir, f"sample{i:03d}.txt")
with open(gcode_filename, "w") as gcode_file:
 gcode = tg.export_gcode(scale=0.1)
 gcode_file.write(gcode)
# Save image
 image_filename = os.path.join(outputdir, f"sample{i:03d}.png")
 tg.save_image(image_filename, target_width=64, target_height=64)
print(f"Saved sample {i:03d}")
# Generate the dataset
generate_dataset(num_samples=100, output_dir="dataset")

I would like to make it so that the file names are written to a metadata file with the structure:
{"file_name": "0001.png", "text": "0001.txt"}

Certainly! I can help you modify your code to generate a metadata file with the structure you've requested. Here's how you can modify the generate_dataset function to create this metadata file:

python

import os
import random
import json
from math import atan2, degrees
from TurtleGraphics import (
    TurtleGraphics,
    Position,
)

# ... (keep the rest of your code as is) ...

def generate_dataset(num_samples=100, output_dir="dataset"):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    metadata = []

    for i in range(num_samples):
        tg = TurtleGraphics(width=64, height=64, feed_rate=1200)
        tg.pen_down()
        generate_random_movements(tg)

        # Save G-code
        gcode_filename = f"sample_{i:04d}.txt"
        gcode_path = os.path.join(output_dir, gcode_filename)
        with open(gcode_path, "w") as gcode_file:
            gcode = tg.export_gcode(scale=0.1)
            gcode_file.write(gcode)

        # Save image
        image_filename = f"sample_{i:04d}.png"
        image_path = os.path.join(output_dir, image_filename)
        tg.save_image(image_path, target_width=64, target_height=64)

        # Add metadata entry
        metadata.append({
            "file_name": image_filename,
            "text": gcode_filename
        })

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

This modified version of the generate_dataset function does the following:

    It creates a list called metadata to store the information for each sample.
    Inside the loop, it generates filenames with four-digit numbers (e.g., "0001" instead of "001") to match your desired format.
    After saving each image and G-code file, it adds an entry to the metadata list with the structure you requested.
    After generating all samples, it creates a metadata file named "metadata.jsonl" in the output directory.
    It writes the metadata to the file in JSON Lines format, where each line is a valid JSON object. This format is often more convenient for large datasets as it allows for easy reading line by line.

The resulting metadata file will look like this:

{"file_name": "sample_0000.png", "text": "sample_0000.txt"}
{"file_name": "sample_0001.png", "text": "sample_0001.txt"}
{"file_name": "sample_0002.png", "text": "sample_0002.txt"}
...

This format allows for easy parsing and is compatible with many data processing tools. Each line is a valid JSON object, making it simple to read and process the metadata file.

Would you like me to explain any part of this modification or suggest any further improvements?
Claude does not have the ability to run the code it generates yet.
Claude can make mistakes. Please double-check responses.


Subscribe to Pro for 5x more usage with Claude 3.5 Sonnet.
Subscribe to Pro
