import itertools

# GLOBALS (if you want to access them afterwards)
max_dice, number_of_dice, conditions, roll_list, condition_sum_list, condition_sum_list_false = [None]*6

def main():
    global max_dice, number_of_dice, conditions, roll_list, condition_sum_list, condition_sum_list_false
    max_dice = int(input("How many faces does the die have? ")) # max_dice = 6
    dice_faces = range(1, max_dice+1) # dice_faces = [1, 2, 3, 4, 5, 6]
    number_of_dice = int(input("How many dice do you want to roll? ")) # number_of_dice = 3
    conditions = input("What are the checks you are looking for (separate the numbers by spaces, e.g. 4 5)? ") # separate numbers with spaces
    conditions = sorted([int(i) for i in conditions.split()])

    def condition(roll):
        # How this works:
        # The roll is sorted, afterwards we check each condition.
        # If a dice in the roll matches the 1st condition, that dice is removed from the list
        # and we check the next condition.
        # This keeps going until we exaust the condition loop (whether we removed anything or not)
        # We then check how many elements were removed from the roll; if the number of elements
        # removed matches the number of elements in the condition, then it matches the conditions
        
        original_length = len(roll)
        roll = sorted(roll)
        
        for check in conditions:
            for dice in roll:
                if dice >= check:
                    roll.remove(dice)
                    break
        
        if (len(roll)+len(conditions)) == original_length:
            return True
        else:
            return False

    roll_list = [roll for roll in itertools.product(dice_faces, repeat=number_of_dice)]

    values = set(roll_list)
    total_sum = len(values)
    condition_sum = sum(1 if condition(roll) else 0 for roll in values) # https://stackoverflow.com/questions/2643850/what-is-a-good-way-to-do-countif-in-python
    condition_sum_list = [roll for roll in values if condition(roll)]
    condition_sum_list_false = [roll for roll in values if not condition(roll)]
    print("You rolled {} d{}.".format(number_of_dice, max_dice))
    print("Number of valid combinations (+{}) / total combinations".format(', +'.join([str(x) for x in conditions])))
    print("{}/{} = {:.2%}".format(condition_sum, total_sum, condition_sum/total_sum))

    prompt = input("Press Enter to keep checking other combinations, or write anything and press Enter to stop: ")
    if prompt == "":
        print("")
        return True
    else:
        print("You can rerun the program by writing main() and then Enter.")
        print("You can access the previous run's results by writing the global variables' names and pressing Enter.")
        print("max_dice, number_of_dice, conditions, roll_list, condition_sum_list, condition_sum_list_false")
        return False

if __name__ == "__main__":
    while main():
        pass
