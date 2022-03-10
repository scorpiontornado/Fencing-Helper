class Poule:
  '''
  A poule is a group of fencers that verse each other in a round-robin type format, where each fencer bouts every other fencer once. 

  Attributes:
    + fencer_id[]: keys (parallel to the rows/columns, used to find which fencer is at which row/column)
    + String[][]: raw_data (user input into scorecard)
  '''
  pass

class Round:
  '''
  Essentially one "week" of an event, consisting of poules (groups of fencers). Assigns fencer (ids) to poules based on rankings, analyses the raw data from a poule
  
  Attributes:
    + dict: metadata (contains dates the round occured over)
    + fencer_id[]: prev_ranks (rankings from the previous round, sorted in desc. order, best to worst)
    + fencer_id[]: new_ranks (rankings generated from this round, sorted in desc. order, best to worst)
    + dict: fencer_data (contains wins (w), losses (l), hits gained (hg), hits received (hr), and indicator (ind; hg - hr) for each fencer)
    + int: num_poules (ideally enough to ensure 6 or 7 fencers are in each poule)
    + Poule[]: poules
  
  Methods:
    + allocate_poules() (Allocates fencers into poules based on their rankings from the previous round)
    + display_poules([poule_num]) (poule_num can be "all" (default) or any integer >= 0 and < self.num_poules)
    + parse_data() (Extracts and calculates data (w, l, hg, hr, ind) for each fencer)
    + generate_rankings() (Ranks fencers in desc. order based on data from parse_data)
  '''
  # TODO: Should fencers be here or in year? Should be easy enough to change, just pass in fencers to input. But, do I want changes to fencers here to affect fencers globally?
  def __init__(self, parent, metadata, prev_ranks):
    ''' Input: metadata (dict with key "date"), rankings (list of fencers, sorted in desc. order (i.e. best to worst), from the previous round) '''
    self.parent = parent # Parent (Event) object
    
    self.metadata = metadata # TODO: should the date key be a string YYYYMMDD, DDMMYYYY, or a datetime object?
    self.prev_ranks = prev_ranks

  def allocate_poules(self, num_poules=None):
    '''
    Allocate fencers to poules based on their rankings. Done in a manner that spreads out the top fencers as much as possible.
  
    For example, when inputted 12 fencers, it will place them in poules like so (where each sub-list is a poule, and each number is the fencer's rank):
      [[1, 10, 11], [2, 9, 12], [3, 8], [4, 7], [5, 6]]

    Input: [num_poules] (must be an int, > 0 and <= len(self.prev_ranks))
    '''

    # TODO: determine num_poules automatically, but have some sort of override
    # Need to come up with an algorithm/expression to determine num_poules
    # Ideally, you want there to be 6 or 7 fencers per poule in competition fencing

    # TODO: allocate fencers to Poule objects rather than a 2-D list

    self.DEFAULT_NUM_FENCERS = 6 # the default number of fencers per poule. Usu. 6-7
    
    if (num_poules
        and isinstance(num_poules, int)
        and num_poules > 0
        and num_poules <= len(self.prev_ranks)):
          self.num_poules = num_poules
    else:
      self.num_poules = len(self.prev_ranks) // self.DEFAULT_NUM_FENCERS
    
    self.poules = [[] for _ in range(self.num_poules)] # Create empty poules
    # print("\nEmpty self.poules:", self.poules)
    # print("self.prev_ranks:", self.prev_ranks)
  
    index_from = 0
    index_to = 0 # Poule index_to put the fencer in
    direction = 1 # +1 for forwards, -1 for backwards. The number index_to is incremented by.
  
    while index_from < len(self.prev_ranks):
      # 1. Assign fencer to poule
      self.poules[index_to].append(self.prev_ranks[index_from])
  
      # 2. Increment index_from by 1
      index_from += 1
      
      # 3. Increment index_to by direction
      index_to += direction
      
      # 4. Check if index_to has gone over the boundaries, if so, reset to boundary and change direction
      # (Checking > rather than >= 0 ensures it won't be true on the first pass through, when index_to is 0)
      if index_to > self.num_poules - 1: # check uppper boundary
        index_to = self.num_poules - 1 # reset to upper boundary
        direction = -1 # go down
      elif index_to < 0: # check lower boundary
        index_to = 0 # reset to lower boundary
        direction = 1 # go up

  def display_poules(self, poule_num="all"):
    '''
    Displays the fencer ids in the given poule.
    Input: poule_num (can be "all" (default) or any integer >= 0 and < self.num_poules)
    '''
    if isinstance(poule_num, str) and poule_num.lower() == "all": # check to see if the user wants to display all poules. isinstance is necessary (to check that the input is a string) as integers dont have a .lower() method
      for i, cur_poule in enumerate(self.poules):
        print(f"\n ========= Poule {i+1} =========")
        for fencer_id in cur_poule:
          fencer = self.parent.get_fencer_by_id(fencer_id)
          print(fencer)
    elif isinstance(poule_num, int) and poule_num >= 0 and poule_num < self.num_poules:
      print(f"\n ========= Poule {poule_num} =========")
      for fencer_id in self.poules[poule_num-1]: # -1 because users will expect it to be 1-indexed rather than 0-indexed
        fencer = self.parent.get_fencer_by_id(fencer_id)
        print(fencer)
    else:
      print("Invalid poule number")
  
class Fencer:
  '''
  A single fencer, containing data for the current round only

  Attributes:
    + String: fencer_id ("ID" + integer, e.g. "ID25")
    + String: name
  '''

  def __init__(self, name, fencer_id):
    ''' Initiate variables '''
    self.fencer_id = fencer_id
    self.name = name

  def __str__(self):
    ''' Returns fencer's name and id (justified into columns for readability) when __str__, print(), or str() are called on the object'''
    return '{0.name:<24} {0.fencer_id:<10}'.format(self) # left-justify name and right-justify fencer_id
    
class Event:
  '''
  A single event, such as "years 10-12" or "epee teams event" for "U14", stored within a dictionary of years. 

  Attributes:
    + dict of Strings: event_data
    + Fencer[]: fencers
    + Round[]: rounds
    
  Methods:
    + generate_id()
    + new_round(metadata, [id_rankings])
    + Fencer: get_fencer_by_id(fencer_id)
  '''
    
  def __init__(self, event_data, rankings_file):
    self.event_data = event_data # including keys ("school_years" or "age_bracket"), "weapon", and "type" (individual or group)

    ### Read in the rankings of just the fencers' names (not their IDs) inputted by a coach into a file
    self.fencers = []
    self.highest_id = 0 # Keeps track of the highest integer currently in use in a fencer id. First fencer will have an id of "ID001" # TODO: decide whether to pad with 0s or not # sure, makes it easier to read
    with open(rankings_file) as f:
      for name in f:
        self.highest_id = self.highest_id + 1 # Increment highest_id by 1

        self.fencers.append(Fencer(name.strip(), self.generate_id())) # Append the current name to name_rankings, stripped of newline characters
      
    ### Initialise self.id_rankings (as self.fencers is already ordered by rank initially)
    self.id_rankings = [fencer.fencer_id for fencer in self.fencers]
    self.rounds = []

  def generate_id(self):
    ''' Generates a unique fencer_id, padded with zeros '''
    # Number of 0s to pad with
    padding = 3 - len(str(self.highest_id))
    if padding < 0: padding = 0 # padding is 0 minimum, if the number of digits is 3 or more. E.g. "ID2063"
  
    return "ID" + "0"*padding + str(self.highest_id)

  def new_round(self, metadata, id_rankings=[]):
    '''
    Appends a new round to self.rounds
    Inputs: metadata (dict with key "date"), [id_rankings]
    id_rankings overrides the existing rankings from the previous round, e.g. if a fencer is sick for that round
    '''
    if id_rankings: self.id_rankings = id_rankings # override the current id rankings stored in the event if passed in a new set of id rankings
    self.rounds.append(Round(self, metadata, self.id_rankings)) # create a new round

  def get_fencer_by_id(self, fencer_id):
    ''' Returns the fencer object associated with the given fencer_id '''
    # Linear search
    for fencer in self.fencers:
      if fencer.fencer_id == fencer_id: return fencer