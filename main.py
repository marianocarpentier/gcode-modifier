import math
import re

# Open the input and output files
input_filename = 'testShape2.gcode'
output_filename = 'testShape2_modified.gcode'

# Initialize a counter for the layers
layer_counter = 0

max_degrees = 11  # degrees
angle_shift = 132
wave_length = 100  # how tall the model is

max_radians = math.radians(max_degrees)
max_y = math.sin(max_radians) * angle_shift  # opposite

# Regex pattern to match lines containing Z values in G0 or G1 commands
z_pattern = re.compile(r'G[01].*Z([+-]?\d*\.?\d+)')

layer_counter = 0
skip_layers = 5

# Open the original G-code file for reading
with open(input_filename, 'r') as input_file:
    # Create a new file to store the modified G-code
    with open(output_filename, 'w') as output_file:
        # Read each line from the original G-code file
        prev_y = 0
        first_z = None
        normalized_first_z = None
        for line in input_file:
            # Write the current line to the new file
            output_file.write(line)

            if line.startswith(';LAYER:'):
                # Increment the layer counter (This works on Cura sliced files only, needs changes for other slicers)
                layer_counter += 1

            match = z_pattern.search(line)
            if match and layer_counter > skip_layers:
                # Extract the Z value and convert it to a float
                z_value = float(match.group(1))
                if not first_z:
                    first_z = z_value
                    normalized_first_z = 2 * math.pi / wave_length * first_z
                z_normalized_rad = 2 * math.pi / wave_length * z_value

                current_y = math.sin(z_normalized_rad - normalized_first_z) * max_y
                a_rotation = math.sin(z_normalized_rad - normalized_first_z) * max_degrees / ((angle_shift - z_value) / angle_shift)

                custom_command = f"G1 A{format(a_rotation, '.5f')}\nG91\nG1 B-1.1 Y{format(current_y - prev_y, '.5f')}\nG90\n;---\n"
                prev_y = current_y
                # Write the custom code to the new file
                output_file.write(custom_command)
                # Increment the counter for the next layer
                layer_counter += 1

print(f"Modified G-code file saved as {output_filename}")
