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
    + fencer_id[]: rankings (sorted in desc. order, best to worst)
    + dict: fencer_data (contains wins (w), losses (l), hits gained (hg), hits received (hr), and indicator (ind; hg - hr) for each fencer)
    + Poule[]: poules
  Methods:
    + parse_data() (Extracts and calculates data (w, l, hg, hr, ind) for each fencer)
    + generate_rankings() (Ranks fencers in desc. order based on data from parse_data)
  '''
  # TODO: Should fencers be here or in year? Should be easy enough to change, just pass in fencers to input. But, do I want changes to fencers here to affect fencers globally?
  def __init__(self, rankings):
    ''' Input: rankings - list of fencers, sorted in desc. order (i.e. best to worst), from the previous round '''
    self.rankings = rankings

class Fencer:
  '''
  A single fencer, containing data for the current round only

  Attributes:
    + String: fencer_id ("ID" + integer, e.g. "ID25")
    + String: name
  '''

  def __init__(self, name, old_highest_id):
    ''' Initiate variables, incl. generating a unique fencer id '''
    new_highest_id = old_highest_id + 1
    self.fencer_id = "ID" + new_highest_id
    
    self.name = name

    return new_highest_id # TODO: decide whether to increment here or outside

  def __str__(self):
    ''' Return the fencer's name when __str__, print(), or str() are called on the object'''
    return self.name
    
class Event:
  '''
  A single event, such as "years 10-12" or "epee teams event" for "U14", stored within a dictionary of years. 

  Attributes:
    + dict of Strings: event_data
    + Fencer[]: fencers
    + Round[]: rounds
    
  Methods:
    Fencer: get_fencer_by_id(fencer_id)
  '''
  def __init__(self, event_data, rankings_file):
    self.event_data = event_data # including keys ("school_years" or "age_bracket"), "weapon", and "type" (individual or group)

    # Read in the rankings of just the fencers' names (not their IDs) inputted by a coach into a file
    self.name_rankings = []
    with open(rankings_file) as f:
      for name in f:
        self.name_rankings.append(name.strip()) # Append the current name to name_rankings, stripped of newline characters

    # self.rounds = [Round(self.rankings)] # Initialise the rounds with a round with hardcoded rankings (determined by one of the coaches)