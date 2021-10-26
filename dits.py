import shelve
from data_structures import SuburbMap, Suburb, BrunchSpots, Restaurant


### Main


def run_dits():
    greeting()
    main_menu()


### Menus


def main_menu():
    choices = {'modify suburb data': suburb_menu, 'modify restaurant data': restaurant_menu, 'backup data': backup_check, 'quit': goodbye}
    print('\n_____Main Menu_____')
    user_choice("Please choose from one of the following Menu options:", choices)

def suburb_menu():
    choices = {'review data': review_suburbs, 'add new suburb': add_suburb, 'add suburb adjacencies': add_adjacents,'backup data': backup_check, 'quit': goodbye}
    print('\n_____Suburb Data Menu_____')
    user_choice("Please choose from one of the following Menu options:", choices)    

def restaurant_menu():
    choices = {'review data': review_restaurants, 'add new restaurant': add_restaurant, 'main menu': main_menu, 'quit': goodbye}
    print('\n_____Restaurant Data Menu_____')
    user_choice("Please choose from one of the following Menu options:", choices)

def review_suburbs():
    suburb_data, restaurant_data = load_data()
    print('\nSuburbs: \n{0}'.format(suburb_data))
    main_menu()

def review_restaurants():
    suburb_data, restaurant_data = load_data()
    print('\n{0}'.format(restaurant_data))
    main_menu()


### Suburb Functions


def add_suburb():
    suburb_map, restaurant_data = load_data()
    burbs_to_add = clean_input(f'List the suburbs to add seperated by commas:\n')
    burbs_to_add_list = [burb.strip() for burb in burbs_to_add.split(',')]
    for burb in burbs_to_add_list:
        new_suburb = Suburb(burb)
        suburb_map.add_suburb(new_suburb)
    save_data(suburb_map, restaurant_data)
    print('Thank you for updating the suburb lists.')
    choices = {'add more suburbs': add_suburb, 'add adjacencies': add_adjacents, 'main menu': main_menu, 'quit': goodbye}
    user_choice('Would you like to add any more suburbs or adjacency details?:', choices)

def add_adjacents():
    suburb_data, restaurant_data = load_data()
    from_burb = clean_input('What suburb do you want to add adjacent suburbs to?:\n' )
    if from_burb not in suburb_data.graph_dict:
        print(f'''
        Either {from_burb.title()} does not yet exist in database or there has been a typo.
        Please check input for typos or add {from_burb.title()} as a new suburb
        ''')
        add_adjacents()
    print('Suburbs already listed as adjacent:', [burb.name.title() for burb in suburb_data.graph_dict[from_burb].get_burbs()])
    burbs_to_add = clean_input(f'List the suburbs adjacent to {from_burb.title()} seperated by commas:\n')
    burbs_to_add_list = [burb.strip() for burb in burbs_to_add.split(',')]
    suburb_data.add_adjacent(suburb_data.graph_dict[from_burb], burbs_to_add_list)
    save_data(suburb_data, restaurant_data)
    choices = {'yes': add_adjacents, 'no': main_menu}
    user_choice('Would you like to add more adjacencies?:', choices)


### Restaurant Functions


def add_restaurant():
    choices = {'add restaurant': add_restaurant, 'restaurant data menu': restaurant_menu, 
            'main menu':main_menu, 'quit': quit}
    suburb_data, restaurant_data = load_data()
    r_name = clean_input('What is the name of the restaurant?\n')
    if r_name in restaurant_data.get_spots_list():
        print('''That restaurant is already on record!''')
        user_choice('Would you like to add another restaurant?', choices)
    r_address = clean_input('What is the street address?(without suburb or city)\n')
    r_suburb_input = clean_input('What suburb is the restaurant in?\n')
    r_suburb_input = check_valid_burb(r_suburb_input, suburb_data)
    r_suburb = suburb_data.graph_dict[r_suburb_input]
    r_has_view = clean_input('Does it have a nice view?(True/False)\n').title()
    if r_has_view == 'True':
        r_has_view = True
        r_view = clean_input('View type?(ie Seaside or Garden)\n')
    else:
        r_has_view = False
        r_view = None
    r = Restaurant(r_name, r_address, r_suburb, r_has_view, r_view)
    restaurant_data.add_brunch_spot(r)
    suburb = suburb_data.graph_dict[r_suburb_input]
    suburb.add_restaurant_in_burb(r)
    print(r)
    print(suburb.get_spots())
    save_data(suburb_data, restaurant_data)
    
    user_choice('Would you like to add another restaurant?', choices)
    


### Utilities


def load_data():
    try:
        file = shelve.open('suburbs_and_restaurants', 'r')
    except: 
        file = shelve.open('suburbs_and_restaurants', 'c')
    try:
        suburb_data = file['suburbs']
    except:
        suburb_data = SuburbMap(clean_input('\nWhat city is this app for: \n'))
    try:
        restaurant_data = file['restaurants']
    except:
        restaurant_data = BrunchSpots(f'{suburb_data.name} Brunch Spots')
    file.close()

    return suburb_data, restaurant_data
        
def save_data(suburb_map, restaurant_data):
    file = shelve.open('suburbs_and_restaurants', 'w')
    file['restaurants'] = restaurant_data
    file['suburbs'] = suburb_map
    file.close()

def backup_check():
    choices = {'proceed': make_backup, 'cancel': main_menu}
    user_choice('ANY EXISTING BACKUP WILL BE OVERWRITTEN!!!\nAre you sure you want to proceed?', choices)

def make_backup():
    suburb_data, restaurant_data = load_data()
    try:
        file = shelve.open('Brunchify_Backup_File', 'c')
    except Exception as exception:
        print('Script encountered an error generating backup file.\n',exception)
        return
    file['restaurants'] = restaurant_data
    file['suburbs'] = suburb_data
    print('\nSuccess! Backup Created!\n')
    main_menu()


### Helper Functions

def check_valid_burb(suburb, suburb_map):
    if suburb in suburb_map.graph_dict:
        return suburb
    else:
        suburb = clean_input('''Sorry, that suburb is not on record.
        Please input an existing suburb: ''')
        return check_valid_burb(suburb, suburb_map)

def clean_input(question):
    answer = input(question).lower().strip()
    if answer =='':
        print("Sorry, we didn't get that.")
        return clean_input(question)
    return answer

def user_choice(question, options):
    options_list = [option.title() for option in options]
    options_str = " -- ".join(options_list)
    answer = input(question + '\n' + options_str + '\n').lower().strip()
    if answer =='':
        print("Sorry, we didn't get that.")
        return user_choice(question, options)
    elif answer in options:
        options[answer]()
    else:
        print("Sorry, that isn't an option from this menu.")
        return user_choice(question, options)

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
Data Input Terminal Service!
''')
    input('Press Enter to Quit')












restaurant_menu()