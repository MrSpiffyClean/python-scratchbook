import itertools

def condition(roll):
    # sort by value
    # check one by one, if checks, check another
    # if both checks, then true, else false
    original_length = len(roll)
    conditions = [4,5]
    
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

max_dice = 6
dice_faces = range(1, max_dice+1) # dice_faces = [1, 2, 3, 4, 5, 6]
number_of_dice = 3

roll_list = [roll for roll in itertools.product(dice_faces, repeat=number_of_dice)]

values = set(roll_list)
total_sum = len(values)
condition_sum = sum(1 if condition(roll) else 0 for roll in values) # https://stackoverflow.com/questions/2643850/what-is-a-good-way-to-do-countif-in-python
print(f"{condition_sum}/{total_sum} = {condition_sum/total_sum}")
