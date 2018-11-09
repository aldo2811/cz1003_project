# for database formatting, please refer to module/data.py

import module.convert as convert
import module.transport as transport


def assign_dist(user_location, database):
    """Assigns distance from user to each canteen to the database.

    Args:
        user_location ((x, y); tuple): Location that user marked on the map.
        database (dict): Canteen database.

    Returns:
        database (dict): Canteen database that has been assigned with the distance to user.
    """
    list_dict = list(database.keys())
    for i in list_dict:
        current_dist = transport.distance_a_b(user_location, i[1])
        database[i][2] = convert.pixel_to_meter(current_dist)
    return database


def by_distance(user_location, database):
    """Sorts the database by distance, from the nearest to furthest from user.

    Args:
        user_location ((x, y); tuple): Location that user marked on the map.
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by distance to user.
    """
    database = assign_dist(user_location, database)
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
    category = sorted(database.items(), key=lambda tup: tup[0][3])
    return convert.list_to_dict(category)


def by_price(database):
    """Sorts the database by price, from the cheapest to most expensive.

    Args:
        database (dict): Canteen database.

    Returns:
        dict: Canteen database that has been sorted by price.
    """
    sortedprice = sorted(database.items(), key=lambda tup: tup[1][1])
    return convert.list_to_dict(sortedprice)
