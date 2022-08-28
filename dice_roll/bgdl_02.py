import itertools
import json
import random

# GLOBALS (if you want to access them afterwards)
max_dice, number_of_dice, conditions = [None]*3
sample_size = None

def main():
    global max_dice, number_of_dice, conditions, roll_list
    max_dice = int(input("How many faces does the die have? ")) # max_dice = 6
    dice_faces = range(1, max_dice+1) # dice_faces = [1, 2, 3, 4, 5, 6]
    number_of_dice = int(input("How many dice do you want to roll? ")) # number_of_dice = 3
    conditions = input("What are the checks you are looking for (separate the numbers by spaces, e.g. 4 5)? ") # separate numbers with spaces

    def condition_decoder(condition):
        ''' Converts the text input into ranges
        3 different types of input:
        Number (e.g. 4) - Greater or equal to number
        Number followed by sign (e.g. 4-) - Depends on sign. Negative means Lesser or equal to
        List (e.g. [1,2,4,5] ) - What it is on the list
        '''
        
        if condition.startswith('['): # use JSON dumps
            return json.loads(condition)
        elif condition.endswith('-'):
            return range(1, int(condition[0:-1])+1)
        elif condition.endswith('+'):
            return range(int(condition[0:-1]), max_dice+1)
        else:
            return range(int(condition), max_dice+1)

    conditions = [condition_decoder(condition) for condition in conditions.split()]

    def condition(roll):
        # How this works:
        # The roll is sorted, afterwards we check each condition.
        # If a dice in the roll matches the 1st condition, that dice is removed from the list
        # and we check the next condition.
        # This keeps going until we exaust the condition loop (whether we removed anything or not)
        # We then check how many elements were removed from the roll; if the number of elements
        # removed matches the number of elements in the condition, then it matches the conditions

        roll = sorted(roll)
        
        for check in conditions:
            for dice in roll:
                if dice in check:
                    roll.remove(dice)
                    break
        
        if (len(roll)+len(conditions)) == number_of_dice:
            return True
        else:
            return False

    def random_product(*args, repeat=1): # random_product() from itertools recipes in https://docs.python.org/3/library/itertools.html
        "Random selection from itertools.product(*args, **kwds)"
        pools = [tuple(pool) for pool in args] * repeat
        return tuple(map(random.choice, pools))

    def sampler(num = 0):
        while num:
            yield random_product(dice_faces, repeat=number_of_dice)
            num -= 1

    global sample_size

    total_sum = max_dice**number_of_dice
    random_sampling = False
    if total_sum < sample_size:
        condition_sum = sum(map(condition, itertools.product(dice_faces, repeat=number_of_dice))) # quantify() from itertools recipes in https://docs.python.org/3/library/itertools.html
    else: # use random sampling
        random_sampling = True
        condition_sum = sum(map(condition, sampler(sample_size)))

    # use itertools islice for threading

    print("You rolled {} d{}.".format(number_of_dice, max_dice))
    if random_sampling:
        print("Too many possibilities {}. Random sampling {} rolls".format(total_sum, sample_size))
        total_sum = sample_size

    print("Number of valid combinations ({}) / total combinations".format(', '.join([str(list(x)) for x in conditions])))
    print("{}/{} = {:.2%}".format(condition_sum, total_sum, condition_sum/total_sum))

    prompt = input("Press Enter to keep checking other combinations, or write anything and press Enter to stop: ")
    if prompt == "":
        print("")
        return True
    else:
        print("You can rerun the program by writing main() and then Enter.")
        print("You can access the previous run's results by writing the global variables' names and pressing Enter.")
        print("max_dice, number_of_dice, conditions, sample_size")
        return False

if __name__ == "__main__":
    sample_size = int(input("What is your prefered sample size? "))
    while main():
        pass
