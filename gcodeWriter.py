import math
def create_gcode(start, step, max_degrees, wave_length, angle_shift, filename):
    max_radians = math.radians(max_degrees)
    max_y = math.sin(max_radians) * angle_shift  # opposite
    with open(filename, "w") as file:
        prev_y = 0;
        for z in range(int(start / step), int(wave_length / step + step)):
            z_value = z * step
            z_normalized_rad = 2 * math.pi / wave_length * z_value

            current_y = math.sin(z_normalized_rad) * max_y
            a_rotation = math.sin(z_normalized_rad) * max_degrees

            file.write(f"G1 Z{format(z_value, '.5f')} A{format(a_rotation, '.5f')}\nG91\nG1 Y{format(current_y - prev_y, '.5f')}\nG90\n")

            prev_y = current_y

if __name__ == '__main__':
    num_sines = 2
    start = 0  # Start of the range
    max_degrees = 8  # degrees
    step = 0.2  # Step size for iteration
    filename = "test.gcode"
    angle_shift = 132
    wave_length = 100  # how tall the model is
    create_gcode(start, step, max_degrees, wave_length, angle_shift, filename)
