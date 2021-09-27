import shelve
from data_structures import SuburbMap, Suburb, BrunchSpots, Restaurant

def greeting():
    print('Welcome to the Data Input Terminal Service!')
    print(
        '''
From this tool you can update 
the Brunchify App with new 
restaurants and suburbs.
''')
    

def goodbye():
    print(
        '''
Thank you for using the 
Data Input Terminal Service
''')

def load_data():
    file = shelve.open('suburbs_and_restaurants', 'r')
    try:
        suburb_data = file['suburbs']
    except:
        suburb_data = SuburbMap(input('What city is this app for: '))
    try:
        restaurant_data = file['restaurants']
    except:
        restaurant_data = BrunchSpots(f'{suburb_data.name} Brunch Spots')
    file.close()

    return suburb_data, restaurant_data
        

def save_data(suburb_map, brunch_spot_data):
    file = shelve.open('suburbs_and_restaurants', 'w')
    file['restaurants'] = brunch_spot_data
    file['suburbs'] = suburb_map
    file.close()
    

def add_suburb():
    suburb_map, brunch_spots = load_data()
    new_suburb = Suburb(
        input('What is the name of the suburb you want to add?: ').lower().strip()
    )
    suburb_map.add_suburb(new_suburb)
    save_data(suburb_map, brunch_spots)
    choice =input('Would you like to add another suburb?(yes/no): ').lower().strip()
    if choice in 'yes':
        add_suburb()
    else:
        print('Thank you for updating the suburb lists')
        print(suburb_map)

def add_adjacents():
    suburb_data, brunch_spots = load_data()

    start_burb = input('What suburb do you want to add adjacent suburbs to?:\n' ).lower()
    burbs_to_add = input(f'List the suburbs adjacent to {start_burb.title()} seperated by commas:\n').lower()
    burbs_to_add_list = [burb.strip() for burb in burbs_to_add.split(',')]
    for burb in burbs_to_add_list:
        suburb_data.add_adjacent(suburb_data.graph_dict[start_burb], suburb_data.graph_dict[burb])
    
    save_data(suburb_data, brunch_spots)
    review()

def view_or_update():
    choice = input('Would you like to view the existing data or make changes?(review/change): \n').lower().strip()
    if choice in 'review':
        review()
    elif choice in 'change':
        what_to_update()
    else:
        print("Sorry, we didn't get that.")
        view_or_update()

def review():
    suburb_data, restaurant_data = load_data()
    print('Suburbs: \n{0}'.format(suburb_data))
    

def what_to_update():
    print('What would you like to update?')
    update = input('Restaurants or Suburbs?: \n').lower().strip()
    if update == 'restaurants':
        add_restaurant()
    elif update == 'suburbs':
        choice = input('Would you like to add new suburbs or update adjacency?(new/adj): \n').lower().strip()
        if choice == 'new':
            add_suburb()
        elif choice == 'adj':
            add_adjacents()
    else:
        print("Hmm, seems that wasn't one of the recognised options...")
        proceed = input('Quit or Update?: \n').lower().strip()
        if proceed == 'quit':
            return
        elif proceed == 'update':
            what_to_update()
        else:
            run_dits()


def run_dits():
    greeting()
    view_or_update()
    goodbye()


run_dits()