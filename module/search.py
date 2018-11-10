"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

import module.convert as convert


def by_price(foodlist_canteens, price):
    """Filters the database according to maximum price specified by user.

    Args:
        foodlist_canteens (dict): Canteen database.
        price (float): Maximum price specified by user input.

    Returns:
        The database but only with stalls that have an average price less than the specified maximum value.
    """
    pricelist = []
    for key, value in foodlist_canteens.items():
        # value[1] is the average price of the stall
        if value[1] <= price:
            pricelist.append((key, value))
    # convert to database format
    return convert.list_to_dict(pricelist)


def by_food(foodlist_canteens, foodname):
    """Filters the database according to category.

    Args:
        foodlist_canteens (dict): Canteen database.
        foodname (str): Category specified by user input.

    Returns:
        The database but only with stalls that has the same category as the one specified by the user.
    """
    foodlist = []
    for key, value in foodlist_canteens.items():
        # key[3] is the category of the stall
        if key[3].lower() == foodname.lower():
            foodlist.append((key, value))
    # convert to database format
    return convert.list_to_dict(foodlist)
