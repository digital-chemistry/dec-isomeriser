# Author: Aleksandar Kondinski
# License: MIT
# Version: 1.0.0

from itertools import combinations

y_rotation = {1: 2, 2: 1, 3: 4, 4: 3, 5: 10, 6: 9, 7: 8, 8: 7, 9: 6, 10: 5}
x_rotation = {1: 3, 3: 1, 2: 4, 4: 2, 5: 6, 6: 5, 7: 8, 8: 7, 9: 10, 10: 9}
z_rotation = {1: 4, 4: 1, 2: 3, 3: 2, 5: 9, 9: 5, 6: 10, 10: 6, 7: 7, 8: 8}

def rotate(config, rotation):
    return [rotation[pos] for pos in config]

def all_rotations(config):
    rotations = set()
    current = config
    
    for _ in range(2):
        current = rotate(current, y_rotation)
        rotations.add(tuple(sorted(current)))
    
    current = config
    for _ in range(2): 
        current = rotate(current, x_rotation)
        rotations.add(tuple(sorted(current)))
    
    current = config
    for _ in range(2): 
        current = rotate(current, z_rotation)
        rotations.add(tuple(sorted(current)))
    
    return rotations

def is_unique(config, seen):
    rotations = all_rotations(config)
    for rotation in rotations:
        if rotation in seen:
            return False
    return True

def generate_combinations_positions(num_boxes, num_black_boxes):
    if num_black_boxes == 0:
        return [[]]
    
    all_combinations = list(combinations(range(1, num_boxes + 1), num_black_boxes))
    unique_combinations = []
    seen = set()

    for comb in all_combinations:
        if is_unique(comb, seen):
            unique_combinations.append(comb)
            seen.add(tuple(sorted(comb)))

    return unique_combinations

def save_combinations_to_file(filename, num_boxes):
    total_combinations = 0
    with open(filename, 'w') as file:
        for i in range(0, num_boxes + 1): 
            combs = generate_combinations_positions(num_boxes, i)
            total_combinations += len(combs)
            file.write(f"Step {i}: {len(combs)} unique combinations\n")
            for comb in combs:
                file.write(f"{list(comb)}\n")
            file.write("\n")
    return total_combinations

num_boxes = 10
output_file = 'combinations.txt'

total_combinations = save_combinations_to_file(output_file, num_boxes)

for i in range(0, num_boxes + 1):
    combs = generate_combinations_positions(num_boxes, i)
    print(f"Step {i}: {len(combs)} unique combinations")

print(f"Total number of unique combinations: {total_combinations}")
