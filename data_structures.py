class SuburbMap:
    def __init__(self, name):
        self.name = name
        self.graph_dict = {}
                
    def __repr__(self):
        burb_list = ''
        for key, value in self.graph_dict.items():
            burb_list += '{0}:\n  '.format(key.title())
            burbs = value.get_burbs()
            for burb in burbs:
                if burb == burbs[-1]:
                    burb_list += '{0}'.format(burb.name.title())    
                else:
                    burb_list += '{0}, '.format(burb.name.title())
            burb_list += '\n'
        return burb_list
        

    def add_suburb(self, suburb):
        if suburb.name in self.graph_dict:
            print('Suburb already on record!')
        else:
            self.graph_dict[suburb.name] = suburb

    def add_adjacent(self, from_burb, burblist):
        burb_vertices = [self.graph_dict[burb] for burb in burblist]
        for adj_burb in burb_vertices:
            if adj_burb.name not in self.graph_dict:
                print(f'''Either {adj_burb.title()} does not yet exist in database or there has been a typo.
                Please check input for typos or add {adj_burb.title()} as a new suburb''')
                continue    
            if from_burb not in adj_burb.get_burbs() and adj_burb not in from_burb.get_burbs():
                self.graph_dict[from_burb.name].add_adjacent(adj_burb)
                self.graph_dict[adj_burb.name].add_adjacent(from_burb)
                print(f'{from_burb.name.title()} and {adj_burb.name.title()} were listed as adjacent to eachother.')
            elif from_burb not in adj_burb.get_burbs() and adj_burb in from_burb.get_burbs():
                self.graph_dict[adj_burb.name].add_adjacent(from_burb)
                print(f'{from_burb.name.title()} was added as adjacent to {adj_burb.name.title()}.')
            elif from_burb in adj_burb.get_burbs() and adj_burb not in from_burb.get_burbs():
                self.graph_dict[from_burb.name].add_adjacent(adj_burb)
                print(f'{adj_burb.name.title()} was added as adjacent to {from_burb.name.title()}.')
            else:
                print(f'{from_burb.name.title()} and {adj_burb.name.title()} are already listed as adjacent.')


class Suburb:
    def __init__(self, name):
        self.name = name
        self.adjacent_suburbs = []
        self.brunch_spots = []

    def add_adjacent(self, suburb):
        self.adjacent_suburbs.append(suburb)

    def add_restaurant_in_burb(self, restaurant):
        if restaurant.name in self.brunch_spots:
            print("A restaurant by that name is already listed in this suburb!")
        else:
            self.brunch_spots.append(restaurant.name)

    def get_spots(self):
        return self.brunch_spots

    def get_burbs(self):
        return self.adjacent_suburbs

class Restaurant:
    def __init__(self, name, street_address, suburb, has_view=False, view=None):
        self.name = name
        self.street_address = street_address
        self.suburb = suburb
        self.has_view = has_view
        self.view = view
        self.brunch = self.add_hours()

    def add_hours(self):
        schedule = {'mon': {}, 'tue': {}, 'wed':{}, 'thu': {}, 'fri': {}, 'sat': {}, 'sun': {}}
        for key in schedule.keys():
            times_to_add = input(f'''\nEnter the brunch menu start time and end time 
for {key.title()} in 24hr format seperated by a hyphen:\n''')
            start_end_list = [int(time.strip()) for time in times_to_add.split('-')]
            schedule[key]['start time'] = start_end_list[0]
            schedule[key]['end time'] = start_end_list[1]
        return schedule

    def __repr__(self) -> str:
        string = '''
{0}:\n  Opening Hours:'''.format(self.name.title())
        for key, value in self.brunch.items():
            string += '\n    {0}: '.format(key.title())
            string += '{0} - {1}'.format(str(value['start time']), str(value['end time']))
        string += '\n  Address:\n    {0}\n    {1}'.format(self.street_address.title(),self.suburb.name.title())
        if self.has_view:
            string += '\n  FYI:\n    {0} has a lovely {1} view.'.format(self.name.title(),self.view)
        return string

class BrunchSpots:
    def __init__(self, name):
        self.name = name
        self.brunch_spots = {}

    def add_brunch_spot(self, restaurant):
        if restaurant in self.brunch_spots.values():
            print('Restaurant already on record!')
        else:
            self.brunch_spots[restaurant.name] = restaurant

    def __repr__(self) -> str:
        string = '\nWellington Brunch Spots:'
        for spot in self.brunch_spots.values():
            string += '\n{0}'.format(spot.__repr__()) 
        return string

    def get_spots_list(self):
        return self.brunch_spots