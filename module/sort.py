"""database format: {(str, (int, int), str, str): [int, float, float, {str: float, str: float...}]}
database key data format: (canteen_name, (canteen_location), stall_name, category)
database value data format: [stall_rating, average_price, distance_to_user, {menu1: price1, menu2: price2...}]
"""

import module.convert as convert
import module.transport as transport


def by_distance(user_location, database):
    """Sorts the database by distance, from the nearest to furthest from user.

    Args:
        user_location ((x, y) -> tuple): Location that user marked on the map.
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by distance to user.
    """
    # tup[1][2] refers to distance from canteen to user
    sort_info = sorted(database.items(), key=lambda tup: tup[1][2])
    return convert.list_to_dict(sort_info)


def by_rank(database):
    """Sorts the database by rank, from the highest to lowest rating.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by rank.
    """
    # tup[1][0] refers to stall rating
    # order is reversed as it sorts rating descending, from highest to lowest
    rank = sorted(database.items(), key=lambda tup: tup[1][0], reverse=True)
    return convert.list_to_dict(rank)


def by_category(database):
    """Sorts the database by category, category is ordered alphabetically.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by category.
    """
    # tup[0][3] refers to category
    category = sorted(database.items(), key=lambda tup: tup[0][3])
    return convert.list_to_dict(category)


def by_price(database):
    """Sorts the database by price, from the cheapest to most expensive.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by price.
    """
    # tup[1][1] refers to average price
    sortedprice = sorted(database.items(), key=lambda tup: tup[1][1])
    return convert.list_to_dict(sortedprice)
