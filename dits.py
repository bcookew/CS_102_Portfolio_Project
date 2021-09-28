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
    input('Press any key to Quit')

def load_data():
    try:
        file = shelve.open('suburbs_and_restaurants', 'r')
    except: 
        file = shelve.open('suburbs_and_restaurants', 'c')
    try:
        suburb_data = file['suburbs']
    except:
        suburb_data = SuburbMap(get_user_input('\nWhat city is this app for: \n'))
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
    
def return_or_quit():
    choice = get_user_input('\nWould you like to return to the main menu or quit?(return/quit):\n')
    if choice in 'quit':
        goodbye()
    elif choice in 'return':
        view_or_update()

def get_user_input(question):
    answer = input(question).lower().strip()
    if answer =='':
        print("Sorry, we didn't get that.")
        return get_user_input(question)
    return answer

def add_suburb():
    suburb_map, brunch_spots = load_data()
    burbs_to_add = get_user_input(f'List the suburbs to add seperated by commas:\n')
    burbs_to_add_list = [burb.strip() for burb in burbs_to_add.split(',')]
    for burb in burbs_to_add_list:
        new_suburb = Suburb(burb)
        suburb_map.add_suburb(new_suburb)
    save_data(suburb_map, brunch_spots)
    review()
    choice = get_user_input('\nWould you like to add more suburbs?(yes/no): \n')
    if choice in 'yes':
        add_suburb()
    else:
        print('Thank you for updating the suburb lists.')
        choice = get_user_input('\nWould you like to add any new adjacency details?(yes/no):\n')
        if choice in 'yes':
            add_adjacents()
        elif choice in 'no':
            return_or_quit()

def add_adjacents():
    suburb_data, brunch_spots = load_data()
    start_burb = get_user_input('What suburb do you want to add adjacent suburbs to?:\n' )
    if start_burb not in suburb_data.graph_dict:
        print(f'''
        Either {start_burb.title()} does not yet exist in database or there has been a typo.
        Please check input for typos or add {start_burb.title()} as a new suburb
        ''')
        add_adjacents()
    print('Suburbs already listed as adjacent:', [burb.name.title() for burb in suburb_data.graph_dict[start_burb].get_burbs()])
    burbs_to_add = get_user_input(f'List the suburbs adjacent to {start_burb.title()} seperated by commas:\n')
    burbs_to_add_list = [burb.strip() for burb in burbs_to_add.split(',')]
    for burb in burbs_to_add_list:
        if burb not in suburb_data.graph_dict:
            print(f'''Either {burb.title()} does not yet exist in database or there has been a typo.
            Please check input for typos or add {burb.title()} as a new suburb''')
            continue
        suburb_data.add_adjacent(suburb_data.graph_dict[start_burb], suburb_data.graph_dict[burb])
    save_data(suburb_data, brunch_spots)
    choice = get_user_input('Would you like to add more adjacencies?(yes/no): ')
    if choice in 'yes':
        add_adjacents()
    else:
        print('Thank you for updating the suburb adjacency lists.')
        return_or_quit()

def view_or_update():
    choice = get_user_input('Would you like to view the existing data or make changes?(review/change): \n')
    if choice in 'review':
        review()
    elif choice in 'change':
        what_to_update()
    else:
        print("Sorry, we didn't get that.")
        view_or_update()

def review():
    suburb_data, restaurant_data = load_data()
    print('\nSuburbs: \n{0}'.format(suburb_data))
    

def what_to_update():
    print('What would you like to update?')
    update = get_user_input('Restaurants or Suburbs?: \n')
    if update in 'restaurants':
        add_restaurant()
    elif update in 'suburbs':
        choice = get_user_input('\nWould you like to add new suburbs or update adjacency?(new/adj): \n')
        if choice in 'new':
            add_suburb()
        elif choice in 'adj':
            add_adjacents()
    else:
        print("\nHmm, seems that wasn't one of the recognised options...")
        proceed = get_user_input('Quit or Update?: \n')
        if proceed in 'quit':
            return
        elif proceed in 'update':
            what_to_update()
        else:
            run_dits()


def run_dits():
    greeting()
    view_or_update()


run_dits()