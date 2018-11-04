def user_input_index(min_index, max_index):
    user_input = input()
    if user_input.isdigit() and min_index <= int(user_input) <= max_index:
        return int(user_input)
    else:
        print("Error! Invalid input!")
        return user_input_index(min_index, max_index)


def user_input_float():
    user_input = input()
    try:
        user_input = float(user_input)
        if user_input < 0:
            return user_input_float()
        else:
            return user_input
    except:
        print("Error! Invalid input!")
        return user_input_float()