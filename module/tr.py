from operator import itemgetter
import math
import module.convert as convert


#plan before coding, research

#calculate distance
def distance_a_b(location_of_a, location_of_b):
    distance_a_b = math.sqrt((location_of_a[0]-location_of_b[0])**2 + (location_of_a[1] - location_of_b[1])**2)
    return distance_a_b

#assigning distance to each canteen
# list is the most easy to ammend, sort etc
#list within list
def assign_dist(user_location, database):
    #cant index dictionary, damn, so i am using list, which will list the keys, inside is tuple, but the tuple inside mutable still not considered a full tuple
    list_dict = list(database.keys())
    for i in list_dict:
        current_dist = distance_a_b(user_location, i[1])
        database[i][2] = current_dist
    return database
##        sort_info = sorted(dist_data)
##    return sort_info    


#sort by distance
#sort the list according to the distance at the from the back
#display
def sort_distance(user_location, database):
    database = assign_dist(user_location, database)
    sort_info = sorted(database.items(), key = lambda tup: tup[1][2])
    return convert.list_to_dict(sort_info)

#itemcan only go by the surface level and hence maximum is 1
#sort by rank
def sort_by_rank(database):
    rank = sorted(database.items(), key = lambda tup: tup[1][0], reverse = True)
    return convert.list_to_dict(rank)

#sort by category
def sort_by_category(database):
    category = sorted(database.items(), key = lambda tup: tup[0][3])
    return convert.list_to_dict(category)


#sort by price
#take out the price, put it to the front of the list
#sort everything by the price
#display



     




#for i,n in zip(list_dict, range(len(length))): use this to update for loops together
#https://stackoverflow.com/questions/9038160/break-two-for-loops to break out 2 for loops




#cannot use cause it will the prices will stick together to 1 canteen        
##        assigned_list = [price_data[x:x+length[count]],i]
##        assigned.append(assigned_list)
##        x += length[count]
##        count += 1
##        print(assigned)
##    return assigned


##        for x in range(length[count]):  =====> cannot use this as once you set it in range, you cannot change it alr
##            print(price_data[x])



        
  

#not using sorted function because it cant sort dictionary, what a joke, convert to list previously for this matter
#try to make the price at the subject
def sort_by_price(database):
    sortedprice = sorted(database.items(), key=lambda tup: tup[1][1])
    return convert.list_to_dict(sortedprice)