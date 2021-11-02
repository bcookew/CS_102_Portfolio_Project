import shelve

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

def clean_input(question, options=None):
    if options == None:
        answer = input(question).lower().strip()
    else:
        answer = input(question + menu_option_formatter(options)).lower().strip()
    if answer =='':
        print("Sorry, we didn't get that.")
        return clean_input(question)
    return answer

def user_choice(question, options):
    answer = input(question + menu_option_formatter(options)).lower().strip()
    if answer =='':
        print("Sorry, we didn't get that.")
        return user_choice(question, options)
    else:
        options[deduction(options, answer)]()
        
def deduction(options, search_term):
        potential_matches = []
        for option in options.keys():
            for option_index in range(len(option)):
                match_count = 0
                for search_index in range(len(search_term)):
                    if search_index + option_index >= len(option):
                        continue
                    elif search_term[search_index] == option[search_index + option_index]:
                        match_count += 1
                    else:
                        break
                if match_count > 1:
                    potential_matches.append(option)
        if len(potential_matches) == 0:
            new_search_term = clean_input("Sorry, your input didn't match an option from this menu. Please try again:" + menu_option_formatter(options))
            return deduction(options, new_search_term)
        elif len(potential_matches) == 1:
            return potential_matches[0]
        else:
            new_search_term = clean_input('Your input matched multiple options please select again.' + menu_option_formatter(potential_matches))
            return deduction(options, new_search_term)
    
def menu_option_formatter(options_list):
    options_list = [option.title() for option in options_list]
    option_string = '\n{0}\n'.format(" -- ".join(options_list))
    return option_string

def header(header):
    print("\n_____{0}_____\n".format(header))