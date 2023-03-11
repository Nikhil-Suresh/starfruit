from collections import deque

with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

datastream = raw_input[0]

buffer = deque()
number_of_characters_received = 0
for received_character in datastream:
    number_of_characters_received  += 1
    buffer.append(received_character)
    if len(buffer) > 4:
        buffer.popleft() # Remove the oldest character from the buffer.
    
    check_for_marker = len(set(buffer)) == 4
    if check_for_marker == True:
        print(f"Marker found at character {number_of_characters_received}!")
        break

