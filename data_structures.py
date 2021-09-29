class SuburbMap:
    def __init__(self, name):
        self.name = name
        self.graph_dict = {}
                
    def __repr__(self):
        burb_list = ''
        for key, value in self.graph_dict.items():
            burb_list += '{0}: '.format(key.title())
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
            print('Suburb already on record.')
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

    def get_burbs(self):
        return self.adjacent_suburbs

class Restaurant:
    def __init__(self, name, street_address, suburb, has_view=False, view=None):
        self.name = name
        self.street_address = street_address
        self.suburb = suburb
        self.has_view = has_view
        self.view = view
        self.brunch = self.update_hours()

    def add_hours():
        schedule = {'mon': {}, 'tues': {}, 'wed':{}, 'thurs': {}, 'fri': {}, 'sat': {}, 'sun': {}}
        for key, value in schedule.items():
            schedule[key]['start time'] = input(f'\nEnter the brunch menu start time for {key.title()} in 24hr format:\n')
        return schedule

class BrunchSpots:
    def __init__(self, name):
        self.name = name
        self.brunch_spots = {}
