def user_input_index(min_index, max_index):
    """Asks user for input and checks if it matches a number in the specified range.

    Args:
        min_index (int): Minimum number of user input.
        max_index (int): Maximum number of user input.

    Returns:
        int: An integer that the user inputs if it satisfies the condition.
        Otherwise it returns itself, keeps on asking the user for input until the condition is satisfied
    """
    user_input = input()

    # range is inclusive, between min_index and max_index
    if user_input.isdigit() and min_index <= int(user_input) <= max_index:
        return int(user_input)
    else:
        print("Error! Invalid input!")
        return user_input_index(min_index, max_index)


def user_input_float():
    """Asks user for input and checks whether it is a float.

    Returns:
        float: User input if it is a positive float number.
        Otherwise it returns itself, keeps on asking the user for input until condition is satisfied.
    """
    user_input = input()
    try:
        user_input = float(user_input)
        
        # in this project, only positive float values are needed,
        # that's why negative float values are considered invalid
        if user_input < 0:
            print("Error! Invalid input!")
            return user_input_float()
        else:
            return user_input
    except:
        print("Error! Invalid input!")
        return user_input_float()


def non_empty_input():
    """Checks whether user input is empty or not. (For string)

    Returns:
        string (str): The input entered by the user.
        Returns itself and keeps on asking for input if input is empty.
    """
    string = input()
    if not string or string.isspace():
        print("Invalid input!")
        return non_empty_input()
    return string