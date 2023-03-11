from operator import methodcaller

with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

#########
# PART 1
#########
cleaned_lines = [item.strip('\n') for item in raw_input]

# Split on ',', then split resulting lists on '-'.
# Example: [['94-95','100-101']] -> [['94', '95], ['100','101]]
elf_pairs = [list(map(methodcaller('split', '-'), pair.split(','))) for pair in cleaned_lines]

def convert_bounds_to_set(bound_list):
    '''
    Example: [['94', '95], ['100','101]] -> [{94, 95}, {100, 101}]
    '''
    lower_bound = int(bound_list[0])
    upper_bound = int(bound_list[1])
    return set(range(lower_bound, upper_bound + 1))

# Convert to ranges and then to sets.
# Example: [['94', '95], ['100','101]] -> [{94, 95}, {100, 101}]
elf_pairs = [list(map(convert_bounds_to_set, pair)) for pair in elf_pairs]

count_of_totally_overlapped_pairs = 0

for pair in elf_pairs:
    first = pair[0]
    second = pair[1]
    # If either range of numbers is a subset of the other...
    count_of_totally_overlapped_pairs += first.issubset(second) or second.issubset(first)

print(f'Number of totally overlapped pairs: {count_of_totally_overlapped_pairs}')

#########
# PART 2
#########
count_of_partially_overlapped_pairs = 0

for pair in elf_pairs:
    first = pair[0]
    second = pair[1]
    # If the intersection between the sets is non-zero, increment
    count_of_partially_overlapped_pairs += 1 if first.intersection(second) else 0

print(f'Number of partially overlapped pairs: {count_of_partially_overlapped_pairs}')