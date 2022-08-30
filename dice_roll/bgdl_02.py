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
    conditions = input("What are the checks you are looking for (separate the numbers by spaces, e.g. 4 5+ 3- [1,3,4])? ") # separate numbers with spaces
    permutations = input("Want to check all permutations of the checks (might be slower, but useful for cases such as '[1,3] [1,2]' that might otherwise be missed) (yes/no)? ")
    permutations = permutations.strip().casefold().startswith('y')

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
        ''' Defines the condition checking algorithm
        How this works:
        1. The roll is sorted (this isn't necessarily needed, but it converts the tuple into a list, which allows removal)
        2. We check every condition against the current set of dice
            - If the condition matches a dice, that dice is removed and we check the next condition
            - If the condition doesn't match any dice, then the conditions can't be met, and we return False
        3. If the loop ends, then all conditions have been met, and we return True
        (inspired by a nicer algorithm found on an excel file, posted on
        https://www.facebook.com/groups/BGDLCommunity/posts/1394654674390499/ by Johan Falk (Simon's Dice Machine))
        '''

        roll = sorted(roll)
        
        for check in conditions:
            break_flag = False
            for dice in roll:
                if dice in check:
                    roll.remove(dice)
                    break_flag = True
                    break
            if break_flag: continue
            return False
        return True

    def condition_with_permutations(base_roll):
        ''' Defines the condition checking algorithm, with condition permutations
        This exists in case of some odd condition combinations that might fail on one way but otherwise work
        Example: 2d6, conditions set at [1,3] [1,2] and a dice roll of (1,3) will fail because the loop digests
        the 1 first leaving 3 which is not catched by the 2nd condition, even though the roll is valid.
        '''
        condition_permutations = itertools.permutations(conditions)
        
        flag = False
        for condition_set in condition_permutations:
            roll = sorted(base_roll)
            for check in condition_set:
                break_flag = False
                for dice in roll:
                    if dice in check:
                        roll.remove(dice)
                        break_flag = True
                        break
                if break_flag: continue
                break_flag = False
            if not break_flag: break #return False
            flag = True
            break #return True

        return flag

    def random_product(*args, repeat=1): # random_product() from itertools recipes in https://docs.python.org/3/library/itertools.html
        "Random selection from itertools.product(*args, **kwds)"
        pools = [tuple(pool) for pool in args] * repeat
        return tuple(map(random.choice, pools))

    def sampler(num = 0):
        while num:
            yield random_product(dice_faces, repeat=number_of_dice)
            num -= 1

    global sample_size

    condition_func = condition
    if permutations: condition_func = condition_with_permutations

    total_sum = max_dice**number_of_dice
    random_sampling = False
    if total_sum < sample_size:
        condition_sum = sum(map(condition_func, itertools.product(dice_faces, repeat=number_of_dice))) # quantify() from itertools recipes in https://docs.python.org/3/library/itertools.html
    else: # use random sampling
        random_sampling = True
        condition_sum = sum(map(condition_func, sampler(sample_size)))

    # use itertools islice for threading

    print("")
    print("You rolled {} d{}.".format(number_of_dice, max_dice))
    if random_sampling:
        print("Too many possibilities {}. Random sampling {} rolls".format(total_sum, sample_size))
        total_sum = sample_size
    if permutations:
        print("Used permutations.")
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
