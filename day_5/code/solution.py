with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

#########
# PART 1
#########
cleaned_lines = [item.strip('\n') for item in raw_input]

stack_contents = []

line_count = -1
for line in cleaned_lines:
    line_count += 1
    if line:
        stack_contents.append(line)
    else:
        break

line_numbers = stack_contents.pop()
movement_instructions = cleaned_lines[line_count + 1:]
movement_instructions = [list(map(int, instruction.split(' ')[1::2])) for instruction in movement_instructions]

# Specify how many characters we expect a single box to be represented by.
BOX_CHAR_SIZE = 3

class Box:
    
    def __init__(self, box_representation):
        self.box_contents = box_representation

    def __repr__(self):
        return self.box_contents

    def __str__(self):
        return self.box_contents

    def __bool__(self):
        """Returns True if the box is not empty, False otherwise."""
        return True if self.box_contents != '   ' else False
    
    def __len__(self):
        return len(self.box_contents)

parsed_boxes = []

# Parse the boxes into a list of lists of Box objects.
for line in stack_contents:
    temp_boxes = [] # Temporary list of strings, representing the boxes.
    i = 0
    while i < len(line):
        temp_boxes.append(line[i:i + BOX_CHAR_SIZE]) # Append the next box to the list.
        i += BOX_CHAR_SIZE + 1 # Move forward the size of one box, then skip the space between boxes.
    parsed_boxes.append(list(map(Box, temp_boxes))) # Map the list of strings to a list of Box objects.
        

class BoxGrid:
    """A class representing the grid of boxes."""
    def __init__(self, boxes):
        self.stacks = [[] for _ in range(len(boxes[0]))]
        self.populate_grid(boxes)
        
    def populate_grid(self, boxes):
        """Populates the grid with the boxes."""
        reversed_boxes = boxes[::-1]
        for line_of_boxes in reversed_boxes:
            i = 0
            while i < len(line_of_boxes):
                box = line_of_boxes[i]
                if box:
                    self.stacks[i].append(box)
                i += 1

    def __repr__(self):
        grid_representation = ''
        max_stack_size = max(list(map(len, self.stacks))) # The maximum size of any stack.
        i = max_stack_size + 1

        while i >= 0:
            for stack in self.stacks: # For each stack...
                if i < len(stack): # If the stack is long enough to have a box at this index...
                    grid_representation += str(stack[i]) + ' ' # Add the box to the grid string.
            i -= 1 # Move to the next row.
            grid_representation += '\n' # Represent the end of the row with a newline.
        return grid_representation
    
    def move_box(self, origin_stack, target_stack):
        """Moves a box from one stack to another.
        Args:
            origin_stack (int): The index of the stack to move the box from.
            target_stack (int): The index of the stack to move the box to.
        
        Returns:
            None
        """
        self.stacks[target_stack ].append(self.stacks[origin_stack].pop())

    def display_grid(self):
        """Displays the grid in a more readable format.
        Useful for debugging.
        """
        for stack in self.stacks:
            print(stack)
    
    def answer(self):
        """Returns the top box of every stack."""
        answer = ""
        for stack in self.stacks:
            answer += str(stack[-1])
        print(answer)

grid = BoxGrid(parsed_boxes)

grid.display_grid()
print('#############')

for instruction in movement_instructions:
    times = instruction[0]
    origin = instruction[1] - 1
    target = instruction[2] - 1

    for _ in range(times):
        grid.move_box(origin, target)
grid.display_grid()
grid.answer()
