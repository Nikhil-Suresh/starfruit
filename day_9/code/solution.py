with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

tail_position = (0,0)
head_position = (0,0)

unexpanded_motions = []
for line in raw_input:
    unexpanded_motions.append(line)

expanded_motions = []
for motion in unexpanded_motions:
    direction, distance = motion[0], int(motion[1:])
    expanded_motions += [direction] * distance

visited_positions = set()
visited_positions.add(tail_position)

movement_dictionary = {
    'U': (0, 1),
    'D': (0, -1),
    'L': (-1, 0),
    'R': (1, 0)
}

def calculate_movement_for_tail(tail_position, head_position):
    x_distance = head_position[0] - tail_position[0]
    y_distance = head_position[1] - tail_position[1]

    assert not x_distance > 2
    assert not y_distance > 2

    x_diff_sign = int(x_distance / abs(x_distance)) if x_distance != 0 else 0
    y_diff_sign = int(y_distance / abs(y_distance)) if y_distance != 0 else 0

    # TODO: This caught me out. The knot was 2 away in both X and Y dimensions.
    # The movement is exactly the same (1/-1, 1/-1), but my if statements were not catching it for ages.
    # Eventually I found many people were caught out on this on Reddit, and quickly realized where I was going wrong.
    # The clue this was happening? I found a case where y_distance == 7, which indicates the tail wasn't following.
    amount_to_move = (0,0)
    if (abs(x_distance) == 1 and abs(y_distance) > 1) or (abs(x_distance) > 1 and abs(y_distance) == 1) or (abs(x_distance) == 2 and abs(y_distance) == 2):
        amount_to_move = (x_diff_sign, y_diff_sign)
    elif abs(x_distance) > 1:
        amount_to_move = (x_diff_sign, amount_to_move[1])
    elif abs(y_distance) > 1:
        amount_to_move = (amount_to_move[0], y_diff_sign)
    return amount_to_move


for motion in expanded_motions:
    x, y = movement_dictionary[motion]
    head_position = (head_position[0] + x, head_position[1] + y)
    amount_to_move = calculate_movement_for_tail(tail_position, head_position)
    tail_position = (tail_position[0] + amount_to_move[0], tail_position[1] + amount_to_move[1])
    visited_positions.add(tail_position)

print(f"Number of visited positions: {len(visited_positions)}")

#########
# Part 2
#########

visited_positions = set()
# We have ten knots now. Let the 0th index represent the head.
# Create a list with ten tuples containing (0,0)
knots = [(0,0) for _ in range(0,10)]

for motion in expanded_motions:
    x, y = movement_dictionary[motion]
    # Begin the operation by moving the head knot.
    knots[0] = (knots[0][0] + x, knots[0][1] + y)
    knot_index = 1 # Start at the second knot.
    while knot_index < len(knots):
        # Select the previous knot.
        prior_knot = knots[knot_index - 1]
        moving_knot = knots[knot_index]
        # Find out how far the current knot should move.
        amount_to_move = calculate_movement_for_tail(moving_knot, prior_knot)
        # Move the knot.
        knots[knot_index] = (knots[knot_index][0] + amount_to_move[0], knots[knot_index][1] + amount_to_move[1])
        knot_index += 1
    visited_positions.add(knots[-1]) # Add the last knot to the set of visited positions.

print(f"Number of visited positions: {len(visited_positions)}")
    


