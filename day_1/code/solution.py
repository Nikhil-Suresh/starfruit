with open(r'..\input\input.txt') as f:
    raw_input = f.readlines() # Yields a list of every line in the input file.

#########
# PART 1
#########

cleaned_items = [item.strip('\n') for item in raw_input]

def sum_calories(input_list):
    i = 0
    elf_calories = [0]
    while i < len(input_list) - 1:
        target  = input_list[i]
        if target:
            elf_calories[-1] += int(target)
        else:
            elf_calories.append(0)
        i +=1
    return elf_calories

calories_per_elf = sum_calories(cleaned_items)
most_calories_on_single_elf = max(calories_per_elf)
print(most_calories_on_single_elf)

#########
# PART 2
#########


all_calorie_amounts_sorted = sorted(calories_per_elf)
calories_for_top_three_elves = all_calorie_amounts_sorted[-3:]
print(sum(calories_for_top_three_elves))
