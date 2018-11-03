red_loop = [["Grad Hall & Hall 11", ], ["Hall 23", ],
            ["Hall 12 & 13", ], ["Lee Wee Nam Library", ],
            ["School of Biological Sciences", ], ["School of Comms Studies", ],
            ["Hall 7", ], ["Innovation Centre", ],
            ["Hall 4", ], ["Hall 1", ],
            ["Canteen 2", ], ["Hall 8 & 9", ],
            ["Hall 11", ]]

blue_loop = [["Opposite Hall 10 & 11", ], ["Opposite Hall 8 & 9", ],
             ["Hall 6", ], ["Opposite Hall 4 & 5", ],
             ["Opposite Innovation Centre", ], ["SPMS", ],
             ["Opposite WKW", ], ["Opposite CEE", ],
             ["Opposite Lee Wee Nam Library", ], ["Opposite Hall 3 & 16", ],
             ["Opposite Hall 14 & 15", ], ["Opposite Hall 23", ]]

# red & blue - find nearest bus stop to user & to canteen
if distance_to_canteen <= distance_to_bus_stop or nearest_to_user == nearest_to_canteen:
    # walk
else:
    # return route of bus stop to nearest bus stop to canteen