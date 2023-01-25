with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

#########
# PART 1
#########


cleaned_lines = [item.strip('\n') for item in raw_input]
throws_paired = [throw.split() for throw in cleaned_lines] # Split each throw.

def map_code_to_throw(throw, code_dict):
    return code_dict[throw]

code_remapping = {'X' : 'A', 'Y' : 'B', 'Z' : 'C'} # Dictionary for remapping the encoded throws to 'A', 'B', 'C' for simplicity.

# Turn the throws to tuples and recode.
# Example: [['A', 'Y']] -> [('A', 'B')]
throws_decoded = [(throw[0], map_code_to_throw(throw[1], code_remapping)) for throw in throws_paired]

# Record point values for throws and round outcomes.
throw_points = {'A' : 1, 'B' : 2, 'C' : 3}
outcome_points = {'win' : 6, 'draw' : 3, 'loss' : 0}

def check_for_win_loss_or_draw(elf_throw, my_throw):
    """
    Returns an outcome given the elf's throw and my throw.
    """
    if elf_throw == 'A' and my_throw == 'C':
        return 'loss'
    elif elf_throw == 'C' and my_throw == 'A':
        return 'win'
    elif elf_throw < my_throw:
        return 'win'
    elif elf_throw > my_throw:
        return 'loss'
    else:
        return 'draw'
    
score = 0
for throw in throws_decoded:
    elf_throw = throw[0]
    my_throw = throw[1]
    round_outcome = check_for_win_loss_or_draw(elf_throw, my_throw)

    score_for_my_throw = throw_points[my_throw]
    score_for_outcome = outcome_points[round_outcome]
    score += score_for_my_throw + score_for_outcome

print('Part 1: ' + str(score))

#########
# PART 2
#########

# A loses to B loses to C loses to A
real_code = {'X' : 'loss', 'Y' : 'draw', 'Z' : 'win'}
ord_values_to_modify = {'win' : 1, 'loss' : -1, 'draw' : 0}

# Convert 'X/Y/Z' to 'loss, draw, win'
# Example [('A', 'X')] -> [('A', 'loss')] 
throws_and_desired_outcomes = [(throw[0], real_code[throw[1]]) for throw in throws_paired]

def set_ord_value_between_65_and_67(lower_bound, higher_bound, total_ord_value):
    """
    I've since realized there's a way to do this way more easily with some simple
    modulo operations, but behold my recursion.

    Example:
    We want to win against an elf that throws 'B' (ord value 66). We would subtract one to get
    'A' (ord value 65).

    For 'A', we can subtract one to get 64. This functions detects that 64 is too low,
    and counts down from the upper bound.

    For example, 64 would be turned to 67. 63 would be 66. 62 would be 65 again.
    """
    if total_ord_value < lower_bound:
        return set_ord_value_between_65_and_67(lower_bound, higher_bound, (higher_bound + 1) - (lower_bound - total_ord_value))
    elif total_ord_value > higher_bound:
        return set_ord_value_between_65_and_67(lower_bound, higher_bound, (lower_bound - 1) + (total_ord_value - higher_bound))
    else:
        return total_ord_value

def get_required_throw_for_outcome(throw_and_outcome, ord_values):
    elf_throw, outcome = throw_and_outcome
    throw_ord_value = ord(elf_throw) + ord_values[outcome]
    ord_value_to_be_between_65_and_67 = set_ord_value_between_65_and_67(65, 67, throw_ord_value)
    return (elf_throw, chr(ord_value_to_be_between_65_and_67))

actual_throws = [get_required_throw_for_outcome(pairing, ord_values_to_modify) for pairing in throws_and_desired_outcomes]

score = 0
for throw in actual_throws:
    elf_throw = throw[0]
    my_throw = throw[1]
    round_outcome = check_for_win_loss_or_draw(elf_throw, my_throw)

    score_for_my_throw = throw_points[my_throw]
    score_for_outcome = outcome_points[round_outcome]
    score += score_for_my_throw + score_for_outcome
print('Part 2: ' + str(score))