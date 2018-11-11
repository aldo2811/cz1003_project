"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

import module.convert as convert


def by_distance(database):
    """Sorts the database by distance, from the nearest to furthest from user.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by distance to user.
    """
    # tup[1][2] refers to distance from canteen to user
    sorted_distance = sorted(database.items(), key=lambda tup: tup[1][2])
    # convert back to dictionary (database format)
    return convert.list_to_dict(sorted_distance)


def by_rank(database):
    """Sorts the database by rank, from the highest to lowest rating.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by rank.
    """
    # tup[1][0] refers to stall rating
    # order is reversed as it sorts rating descending, from highest to lowest
    sorted_rank = sorted(database.items(), key=lambda tup: tup[1][0], reverse=True)
    # convert back to dictionary (database format)
    return convert.list_to_dict(sorted_rank)


def by_category(database):
    """Sorts the database by category, category is ordered alphabetically.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by category.
    """
    # tup[0][3] refers to category
    sorted_category = sorted(database.items(), key=lambda tup: tup[0][3])
    # convert back to dictionary (database format)
    return convert.list_to_dict(sorted_category)


def by_price(database):
    """Sorts the database by price, from the cheapest to most expensive.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by price.
    """
    # tup[1][1] refers to average price
    sorted_price = sorted(database.items(), key=lambda tup: tup[1][1])
    # convert back to dictionary (database format)
    return convert.list_to_dict(sorted_price)