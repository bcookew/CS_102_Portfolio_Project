import shelve
from time import sleep
# User Menus
def main_menu():
    choices = {'about':about, 'search': search_menu, 'quit': end_program}
    users_choice = user_choice('Please type one of the menu options: ', choices)


def about():
    print('''About this app:
    Brunchify Wellington ''')
    main_menu()


def search_menu():
    print('_____Search Menu_____')
    main_menu()
    

def end_program():
    print('_____GOODBYE_____')
    sleep(3)
    exit()

# Utilities
def load_data():
    try:
        file = shelve.open('suburbs_and_restaurants', 'r')
    except: 
        print('Error while retreiving file!!!')
    try:
        suburb_data = file['suburbs']
    except:
        print('Error while retreiving Suburb Data!!!')
    try:
        restaurant_data = file['restaurants']
    except:
        print('Error while retreiving Restaurant Data!!!')
    file.close()
    try: 
        return suburb_data, restaurant_data
    except:
        print('Fatal Error. Data could not be loaded!!!')
        exit()

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
        
        

# Launch Script
suburb_data, restaurant_data = load_data()
main_menu()