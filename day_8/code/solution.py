with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

strings_with_stripped_newlines = [string.strip() for string in raw_input]

grid_width = len(strings_with_stripped_newlines[1])
grid_height = len(strings_with_stripped_newlines)

print(f"Grid width: {grid_width}")
print(f"Grid height: {grid_height}")

tree_grid = []

for row in strings_with_stripped_newlines:
    tree_grid.append(list(map(int, list(row))))

coordinates_to_check = []
for x in range(grid_width):
    for y in range(grid_height):
        coordinates_to_check.append((x, y)) # (x, y) tuples representing all coordinates in the list.

visible_trees = grid_height * grid_width

def compare_coordinates(target_tree_height, coordinates_to_compare, tree_grid):
    """Returns True if any of the trees in the coordinates_to_compare list are taller than the target_tree_height, False otherwise.
    
    Arguments:
        target_tree_height {int} -- The height of the tree we're checking.
        coordinates_to_compare {list} -- A list of (x, y) tuples representing the coordinates of trees to compare against the target tree.
        tree_grid {list} -- A list of lists representing the grid of trees.

    Returns:
        bool -- True if any of the trees in the coordinates_to_compare list are taller than the target_tree_height.
        """
    for (neighbour_x, neighbour_y) in coordinates_to_compare:
        neighbouring_tree_height = tree_grid[neighbour_y][neighbour_x]
        if neighbouring_tree_height >= target_tree_height:
            return True
    return False

# Check each tree in the grid.
for coordinate in coordinates_to_check:
    x, y = coordinate

    if x in {0, grid_width} or y in {0, grid_height}: # Skip the edges of the grid.
        continue

    target_tree_height = tree_grid[y][x]

    # Higher Y represents lower down the grid.
    # Higher X represents further to the right on the grid.
    trees_in_line_above = [coord for coord in coordinates_to_check if coord[0] == x and coord[1] < y]
    trees_in_line_below = [coord for coord in coordinates_to_check if coord[0] == x and coord[1] > y]

    trees_in_line_to_left = [coord for coord in coordinates_to_check if coord[1] == y and coord[0] < x]
    trees_in_line_to_right = [coord for coord in coordinates_to_check if coord[1] == y and coord[0] > x]

    # Check if there are any trees in the lines above, below, to the left and to the right of the target tree.
    found_taller_tree_to_left = compare_coordinates(target_tree_height, trees_in_line_to_left, tree_grid)
    found_taller_tree_to_right = compare_coordinates(target_tree_height, trees_in_line_to_right, tree_grid)
    found_taller_tree_above = compare_coordinates(target_tree_height, trees_in_line_above, tree_grid)
    found_taller_tree_below = compare_coordinates(target_tree_height, trees_in_line_below, tree_grid)

    all_checks = {found_taller_tree_to_left, found_taller_tree_to_right, found_taller_tree_above, found_taller_tree_below}

    # If all checks are True, then the tree is hidden.
    if False not in all_checks:
        visible_trees -= 1
    
print(f"Visible trees: {visible_trees}")