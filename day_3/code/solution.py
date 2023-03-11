with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

#########
# PART 1
#########


cleaned_lines = [item.strip('\n') for item in raw_input]

def split_rucksack(rucksack):
    """
    Return the rucksacks as a list of tuples. Each list element is a rucksack,
    each tuple is a compartment.
    """
    num_items_per_compartment = int(len(rucksack) / 2)
    rucksack_split = (list(rucksack[0:num_items_per_compartment]), list(rucksack[num_items_per_compartment:]))
    return rucksack_split

# Divide up the rucksacks.
divided_rucksacks = list(map(split_rucksack, cleaned_lines))

class RucksackItem:
    """
    On my first read of the question, I didn't note that each item should only be
    counted once, so my first implementation didn't expect to leverage any set-based
    measures.

    __key and __hash__ were implemented upon a re-read, but never used when I realized
    there was a hackier solution.
    """

    def __init__(self, alphabet):
        self.alphabet = alphabet
        raw_ord = ord(alphabet)
        self.priority = raw_ord - 96 if raw_ord >= 97 else raw_ord - 38

    def __str__(self):
        return self.alphabet
    
    def __repr__(self):
        """
        Let's you debug values when viewing a list.
        """
        return f"{self.alphabet} : {self.priority}"

    def __eq__(self, other):
        """
        Enables 'in' syntax.
        """
        return self.alphabet == other.alphabet
    
    def __key(self):
        """
        Enables hashing based on alphabet and priority.
        """
        return (self.alphabet, self.priority)

    def __hash__(self):
        """
        Used to enable being popped into a set.
        """
        return hash(self.__key())


divided_rucksacks_with_priorities = []

# Convert all the characters to RucksackItems.
for rucksack_compartments in divided_rucksacks:
    compartment_1, compartment_2 = rucksack_compartments
    compartment_1 = map(RucksackItem, compartment_1)
    compartment_2 = map(RucksackItem, compartment_2)
    divided_rucksacks_with_priorities.append((list(compartment_1), list(compartment_2)))

priority = 0
for divided_rucksack in divided_rucksacks_with_priorities:
    compartment_1, compartment_2 = divided_rucksack
    for item in compartment_1:
        if item in compartment_2: # __eq__ in RucksackItem enables the 'in' operator.
            priority += item.priority
            # Hack when I realized only one duplicate should count. Just exit the
            # loop whenever you find one item.
            break

print(priority)

#########
# PART 2
#########

# Remove compartments as they aren't used in Part 2, and use sets as we're seeking intersections.
undivided_rucksacks_with_priorities = [set(comp_1).union(set(comp_2)) for comp_1, comp_2 in divided_rucksacks_with_priorities]

group_start = 0
priority = 0
while group_start < len(undivided_rucksacks_with_priorities):
    first_elf = undivided_rucksacks_with_priorities[group_start]
    second_elf = undivided_rucksacks_with_priorities[group_start + 1]
    third_elf = undivided_rucksacks_with_priorities[group_start + 2]
    # Check the intersection of all three sets, then pop the badge out.
    badge = first_elf.intersection(second_elf).intersection(third_elf).pop()
    priority += badge.priority
    group_start += 3 # Move on to the next group (3 elves up the line)

print(priority)



