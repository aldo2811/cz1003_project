from operator import itemgetter
import math


#plan before coding, research

#calculate distance
def distance_a_b(location_of_a, location_of_b):
    distance_a_b = math.sqrt((location_of_a[0]-location_of_b[0])**2 + (location_of_a[1] - location_of_b[1])**2)
    return distance_a_b

#list all distances
def list_of_dist(user_location, database):
    dist_data = []
    #cant index dictionary, damn, so i am using list, which will list the keys, inside is tuple, but the tuple inside mutable still not considered a full tuple
    list_dict = list(database.keys())
    for i in list_dict:
        current_dist = distance_a_b(user_location, i[1])
        dist_data.append(current_dist)
    return dist_data
##        sort_info = sorted(dist_data)
##    return sort_info


#assigning distance to each canteen
# list is the most easy to ammend, sort etc
#list within list
def assign_dist(user_location, database):
    list_dict = list(database.items())
    assigned = []
    count = 0
    dist_data = list_of_dist(user_location, database)
    for i in list_dict:
        assigned_list = [dist_data[count],i]
        assigned.append(assigned_list)
        count += 1
    return assigned        


#sort by distance
#sort the list according to the distance at the from the back
#display
def sort_distance(user_location, database):
    assign_list = assign_dist(user_location, database)
    sort_info = sorted(assign_list, key = itemgetter(0))
    return sort_info

#itemcan only go by the surface level and hence maximum is 1
#sort by rank
def sort_by_rank(database):
    rank = sorted(database.values(), key=itemgetter(0))
    return rank

#sort by category
def sort_by_category(database):
    category = sorted(database.keys(), key=itemgetter(-1))
    return category


#sort by price
#take out the price, put it to the front of the list
#sort everything by the price
#display

def list_of_price(database):
    listprice = list(database.values())
    listpriceextract = []
    length = []
    for i in listprice:
        for n in i[2:]:
            for key,value in n.items():
                x= key
                y= value
                listn = [y,x]
                listpriceextract.append(listn)
        length.append(len(i[2:]))
    return listpriceextract, length



def assign_price(database):
    list_dict = list(database.keys()) #can be keys
    price_data, length = list_of_price(database)
    assigned = []
    x = 0
    old_x = 0
    for i,n in zip(list_dict,range(len(length))):
        while x < old_x + length[n]:
            assignedlst = [price_data[x],i] #i will change after x has finished iterating
            assigned.append(assignedlst)
            x += 1
        old_x = x
    return assigned

     




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
    assignprice = assign_price(database)
    sortedprice = sorted(assignprice, key=itemgetter(0))
    return sortedprice
