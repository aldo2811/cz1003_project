import module.convert as convert


#search database
def search_by_price(foodlist_canteens, price):
    pricelist=[]
    for key, value in foodlist_canteens.items():
        if value[1] <= price:
            pricelist.append((key, value))
    return convert.list_to_dict(pricelist)


#search can_database
#add food items to empty list
#return list
def search_by_food(foodlist_canteens,foodname):
    foodlist=[]
    for key, value in foodlist_canteens.items():
        if key[3].lower() == foodname.lower():
            foodlist.append((key, value))
    return convert.list_to_dict(foodlist)