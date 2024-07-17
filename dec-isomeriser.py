# Author: Aleksandar Kondinski
# License: MIT
# Version: 1.0.0

from itertools import combinations

# Rotation mappings
y_rotation = {1: 2, 2: 1, 3: 4, 4: 3, 5: 10, 6: 9, 7: 8, 8: 7, 9: 6, 10: 5}
x_rotation = {1: 3, 3: 1, 2: 4, 4: 2, 5: 6, 6: 5, 7: 8, 8: 7, 9: 10, 10: 9}
z_rotation = {1: 4, 4: 1, 2: 3, 3: 2, 5: 9, 9: 5, 6: 10, 10: 6, 7: 7, 8: 8}

# Mirror mappings for each direction
z_mirror = {1: 1, 2: 2, 3: 3, 4: 4, 5: 6, 6: 5, 7: 8, 8: 7, 9: 10, 10: 9}
y_mirror = {1: 3, 3: 1, 2: 4, 4: 2, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10}
x_mirror = {1: 2, 2: 1, 3: 4, 4: 3, 5: 9, 6: 10, 7: 7, 8: 8, 9: 5, 10: 6}

# Apply rotation mapping to a given configuration
def rotate(config, rotation):
    return tuple(sorted(rotation[pos] for pos in config))

# Generate all possible rotations of a configuration
def all_rotations(config):
    rotations = {config}
    for rotation_map in [y_rotation, x_rotation, z_rotation]:
        current = rotate(config, rotation_map)
        rotations.add(current)
    return rotations

# Check if a configuration is unique under all rotations
def is_unique(config, seen):
    rotations = all_rotations(config)
    for rotation in rotations:
        if rotation in seen:
            return False
    return True

# Generate unique configurations
def generate_combinations_positions(num_boxes, num_black_boxes):
    if num_black_boxes == 0:
        return [tuple()]

    all_combinations = list(combinations(range(1, num_boxes + 1), num_black_boxes))
    unique_combinations = []
    seen = set()

    for comb in all_combinations:
        if is_unique(comb, seen):
            unique_combinations.append(tuple(sorted(comb)))
            seen.update(all_rotations(comb))

    return unique_combinations

# Find enantiomers based on mirror mappings
def find_enantiomers(configurations):
    enantiomers = []
    config_set = set(configurations)

    for config in configurations:
        for mirror_map in [z_mirror, y_mirror, x_mirror]:
            mirrored_config = rotate(config, mirror_map)
            if mirrored_config in config_set and mirrored_config != config:
                if (mirrored_config, config) not in enantiomers and (config, mirrored_config) not in enantiomers:
                    enantiomers.append((config, mirrored_config))

    return enantiomers

# Save configurations and enantiomers to file
def save_to_file(filename, num_boxes):
    with open(filename, 'w') as file:
        for i in range(num_boxes + 1):
            configurations = generate_combinations_positions(num_boxes, i)
            enantiomers = find_enantiomers(configurations)
            file.write(f"Step {i}: {len(configurations)} unique configurations, {len(enantiomers)} enantiomeric pairs\n")
            for config in configurations:
                if len(config) == 1:  # Single element, remove the comma
                    file.write(f"[{config[0]}]\n")
                else:
                    file.write(f"{list(config)}\n")  # Convert tuple to list for square brackets
            if enantiomers:  # Only write the enantiomer section if there are pairs
                file.write("Enantiomers:\n")
                for pair in enantiomers:
                    # Convert tuples to lists in the output of enantiomer pairs
                    file.write(f"{list(pair[0])} <-> {list(pair[1])}\n")
            file.write("\n")  # This newline ensures there's a blank line between steps
            print(f"Step {i}: {len(configurations)} unique configurations, {len(enantiomers)} enantiomeric pairs")

# Main execution
num_boxes = 10
output_file = 'enantiomers.txt'
save_to_file(output_file, num_boxes)
