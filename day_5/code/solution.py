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
        return True if self.box_contents != '   ' else False
    
    def __len__(self):
        return len(self.box_contents)

parsed_boxes = []

for line in stack_contents:
    temp_boxes = []
    i = 0
    while i < len(line):
        temp_boxes.append(line[i:i + BOX_CHAR_SIZE])
        i += BOX_CHAR_SIZE + 1
    parsed_boxes.append(list(map(Box, temp_boxes)))
        

class BoxGrid:
    
    def __init__(self, boxes):
        self.stacks = [[] for _ in range(len(boxes[0]))]
        self.populate_grid(boxes)
        
    def populate_grid(self, boxes):
        reversed_boxes = boxes[::-1]
        for line_of_boxes in reversed_boxes:
            i = 0
            while i < len(line_of_boxes):
                box = line_of_boxes[i]
                if box:
                    self.stacks[i].append(box)
                i += 1

    def __repr__(self):
        empty_string = ''
        max_stack_size = max(list(map(len, self.stacks)))
        i = max_stack_size + 1

        while i >= 0:
            for stack in self.stacks:
                if i < len(stack):
                    empty_string += str(stack[i]) + ' '
            i -= 1
            empty_string += '\n'
        return empty_string

    def move_box(self, origin_stack, target_stack):
        self.stacks[target_stack ].append(self.stacks[origin_stack].pop())

    def dev_display_grid(self):
        for i in self.stacks:
            print(i)
    
    def answer(self):
        self.string = ""
        for stack in self.stacks:
            self.string += str(stack[-1])
        print(self.string)

grid = BoxGrid(parsed_boxes)

grid.dev_display_grid()

print('#############')

for instruction in movement_instructions:
    times = instruction[0]
    origin = instruction[1] - 1
    target = instruction[2] - 1

    for _ in range(times):
        grid.move_box(origin, target)
grid.dev_display_grid()
grid.answer()