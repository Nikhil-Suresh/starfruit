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

    x_diff_sign = int(x_distance / abs(x_distance)) if x_distance != 0 else 0
    y_diff_sign = int(y_distance / abs(y_distance)) if y_distance != 0 else 0

    amount_to_move = (0,0)
    if (abs(x_distance) == 1 and abs(y_distance) > 1) or (abs(x_distance) > 1 and abs(y_distance) == 1):
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

    


