def list_to_dict(lst):
    """Converts list into dictionary (Specific format).

    Args:
        lst (List): List format: [tuple, tuple].
    
    Returns:
        dic (dict): Dictionary with a key of lst[0] and value of lst[1].
    """
    dic = {}
    for key, value in lst:
        dic[key] = value
    return dic


def pixel_to_meter(distance_in_pixel):
    """Converts distance in pixels into meters (approximation).

    Args:
        distance_in_pixel (float): Distance of 2 points in pixels.

    Returns:
        distance_in_meter (float): Distance of 2 points in meters.
    """
    # after comparing the map with a real map,
    # it is approximated that 1 meter in the real world is equivalent to 1.65 pixels on the map
    distance_in_meter = distance_in_pixel * 1.65
    distance_in_meter = round(distance_in_meter, 2)
    return distance_in_meter


def float_to_dollar(value):
    str_list = ["$"]
    value = "{:.2f}".format(float(value))
    str_list.append(value)
    return "".join(str_list)
