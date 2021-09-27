class SuburbMap:
    def __init__(self, name):
        self.name = name
        self.graph_dict = {}
                
    def __repr__(self):
        burb_list = ''
        for key, value in self.graph_dict.items():
            burb_list += '{0}: {1}\n'.format(key.title(), ', '.join(value.get_burbs()).title())
        return burb_list
        

    def add_suburb(self, suburb):
        self.graph_dict[suburb.name] = suburb

    def add_adjacent(self, from_burb, adj_burb):
        self.graph_dict[from_burb.name].add_adjacent(adj_burb.name)
        self.graph_dict[adj_burb.name].add_adjacent(from_burb.name)

    
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
    def __init__(self, name, open_for_brunch, suburb, has_view=False, view=None):
        self.name = name
        self.brunch = open_for_brunch
        #{'mon': [], 'tues': [], 'wed':[], 'thurs': [], 'fri': [], 'sat': [], 'sun': []}
        self.suburb = suburb
        self.has_view = has_view
        self.view = view

class BrunchSpots:
    def __init__(self, name):
        self.name = name
        self.brunch_spots = {}
