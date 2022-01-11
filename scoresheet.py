class Poule:
  '''
  A poule is a group of fencers that verse each other in a round-robin type format, where each fencer bouts every other fencer once. 

  Attributes:
    + fencer_id[]: key (parallel to the rows/columns, used to find which fencer is at which row/column)
    + String[][]: raw_data (user input into scorecard)
  '''
  pass

class Round:
  '''
  Essentially one "week" of an event, consisting of poules (groups of fencers). Assigns fencer (ids) to poules based on rankings, analyses the raw data from a poule
  
  Attributes:
    + dict: metadata (contains dates the round occured over)
    + fencer_id[]: prev_rankings (rankings from the previous round, sorted in desc. order, best to worst)
    + fencer_id[]: new_rankings (rankings generated from this round, sorted in desc. order, best to worst)
    + dict: fencer_data (contains wins (w), losses (l), hits gained (hg), hits received (hr), and indicator (ind; hg - hr) for each fencer)
    + Poule[]: poules
  
  Methods:
    + allocate_poules() (Allocates fencers into poules based on their rankings from the previous round)
    + parse_data() (Extracts and calculates data (w, l, hg, hr, ind) for each fencer)
    + generate_rankings() (Ranks fencers in desc. order based on data from parse_data)
  '''
  # TODO: Should fencers be here or in year? Should be easy enough to change, just pass in fencers to input. But, do I want changes to fencers here to affect fencers globally?
  def __init__(self, metadata, prev_ranks):
    ''' Input: metadata (dict with key "date"), rankings (list of fencers, sorted in desc. order (i.e. best to worst), from the previous round) '''
    self.metadata = metadata # TODO: should the date key be a string YYYYMMDD, DDMMYYYY, or a datetime object?
    self.prev_ranks = prev_ranks
    
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
    if id_rankings: self.id_rankings = id_rankings # override self.id_rankings if id_rankings is not empty
    self.rounds.append(Round(metadata, self.id_rankings)) # create a new round

  def get_fencer_by_id(self, fencer_id):
    ''' Returns the fencer object associated with the given fencer_id '''
    # Linear search
    for fencer in self.fencers:
      if fencer.fencer_id == fencer_id: return fencer