with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

raw_input = [row.strip() for row in raw_input]

# My first implementation was a little bit messy, and eventually
# I decided the best way to have a high chance of clearing both Part 1
# and Part 2 was to write a pretty direct simulation of the program.
cycle = 0
register = 1
operation_index = 0
target_cycles = {20, 60, 100, 140, 180, 220}
signal_strengths = set()

operation = None
operation_steps_left = 0
value_to_add_to_register = None

# This is a dictionary that maps the operation name to the number of cycles
operation_runtime_dict = {
    'noop': 1,
    'addx': 2,
}

while operation_index < len(raw_input):
    # Saves the signal strength at the specified special cycles.
    if cycle in target_cycles:
        print(f'Cycle {cycle}, register: {register}')
        print(f'Signal strength: {register * cycle}')
        signal_strengths.add(register * cycle)
    
    if operation is None: # When no operation is underway...
        incoming_operation = raw_input[operation_index] # Get the next one. This is incremented at the end of the last loop.
        if incoming_operation == 'noop':
            # This isn't quite optimal, but I was thinking Part 2 might have a new operation.
            operation = 'noop'
            operation_steps_left = operation_runtime_dict[operation]
        else:
            operation, argument =  incoming_operation.split(' ')
            argument = int(argument)
            value_to_add_to_register = argument
            operation_steps_left = operation_runtime_dict[operation]
    
    cycle += 1
    operation_steps_left -= 1 # Decrement the number of cycles left for the current operation.
    if operation_steps_left == 0: # If the operation is complete...
        if operation == 'addx': # Check if it's an addx.
            register += value_to_add_to_register # And if it is, add the stored value to the register.
        operation = None # Then reset the operation.
        operation_index += 1 # And move on to the next operation.
            
print(f'Sum of signal strengths: {sum(signal_strengths)}')

#######
# Part 2
#######
cycle = 0
register = 1
operation_index = 0
signal_strengths = set()

operation = None
operation_steps_left = 0
value_to_add_to_register = None

# I didn't want to use a list of lists because it'd be obnoxious to access the values
# I wanted. So I used a list of strings instead.
pixel_grid = [' ' for _ in  range(40 * 6)]

while operation_index < len(raw_input):
    drawing_range = {register - 1, register, register + 1}
    # This step tripped me up for quite a while!
    # The AOC instructions seemed ambiguous to me, but it looks like
    # the sprite spans EVERY row. The register basically specifies the columns
    # where the sprite is present.
    for i in range(40, 240, 40):
        drawing_range.add(register - 1 + i)
        drawing_range.add(register + i)
        drawing_range.add(register + 1 + i)

    if cycle in drawing_range:
        pixel_grid[cycle] = '#'
    else:
        pixel_grid[cycle] = '.'
    
    # The rest of this is identical to Part 1, so I guess it was smart to simulate the whole process!
    if operation is None:
        incoming_operation = raw_input[operation_index]
        if incoming_operation == 'noop':
            operation = 'noop'
            operation_steps_left = operation_runtime_dict[operation]
        else:
            operation, argument =  incoming_operation.split(' ')
            argument = int(argument)
            value_to_add_to_register = argument
            operation_steps_left = operation_runtime_dict[operation]
    
    cycle += 1
    operation_steps_left -= 1
    if operation_steps_left == 0:
        if operation == 'addx':
            register += value_to_add_to_register
        operation = None
        operation_index += 1


# This is just to print the grid in a readable format.
grid_string = ''
i = 0
for character in pixel_grid:
    grid_string += character
    i += 1
    if i % 40 == 0:
        grid_string += '\n'
print(grid_string)