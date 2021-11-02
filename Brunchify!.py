from time import sleep
from data_structures import BrunchSpots, SuburbMap
from Utils import header, user_choice, deduction, load_data, clean_input

# User Menus
def main_menu():
    header('Main Menu')
    choices = {'about':about, 'search': search_menu, 'quit': end_program}
    user_choice('Please type one of the menu options: ', choices)


def about():
    header('About')
    print(
    '''    Brunchify Wellington 
    ver 1.0
    Created By: Benjamin C Williams

    Brunchify is a portfolio application for exploring data structures
    and recall via processing of user input. Information on restaurant
    opening hours accurate as of 2 Nov 2021''')

    main_menu()


def search_menu():
    header('Search Menu')
    choices = {'search by restaurant name': restaurant_search, 'search by suburb': burb_search}
    user_choice('Please type one of the menu options: ', choices)
    main_menu()
    

def end_program():
    header('GOODBYE')
    sleep(3)
    exit()

def restaurant_search():
    header('Restaurant Search')
    r_searched = clean_input('''Please enter a restaurant name or part thereof or 
type view to return a list of brunch spots with a nice view: ''')
    r = restaurant_data.search_restaurant(r_searched)
    print(r)
    

def burb_search():
    header('Suburb Search')
    searched_burb = clean_input('Please enter a suburb: ')
    
    burb = suburb_data.search_suburb(searched_burb)
    spots = burb.get_spots()
    if len(spots) == 0:
        print('\nSorry, there are no brunch spots currently listed in {0}'.format(burb.name.title()))
    else:
        print("\n" + burb.name.title() + ' Brunch Spots:\n--------------------')

    for spot in spots:
        r = restaurant_data.get_spot(spot)
        print(r)
    
    opts = {'yes':True, 'no':False}
    adjacent = opts[deduction(opts, clean_input('\nWould you like to search the adjacent suburbs as well? ', opts))]
    if adjacent == True:
        adjs = burb.get_burbs()
        regrets = '\nSorry, there are no brunch spots currently listed in:'
        regrets_count = 0
        for adj in adjs:
            spots_adj = adj.get_spots()
            if len(spots_adj) == 0:
                regrets_count += 1
                regrets += "\n  - " + adj.name.title()
                continue
            print("\n" + adj.name.title() + ' Brunch Spots:\n--------------------')
            for spot in spots_adj:
                r = restaurant_data.get_spot(spot)
                print(r)
        if regrets_count > 0:
            print(regrets)
    
    

# Launch Script
suburb_data, restaurant_data = load_data()
main_menu()