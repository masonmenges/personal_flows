from random import randint

def random_type():
    type_list = ['fire', 'grass', 'rock', 'ground', 'water', 'dragon']

    rand_num = randint(0, (len(type_list) - 1))

    return type_list[rand_num]

