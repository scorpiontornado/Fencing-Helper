class Fencer:
  '''
  A single fencer, containing data for the current round only

  Attributers:
    + String: fencer_id ("ID" + integer)
    + String: name
    + dict: data
  '''

  def __init__(self, name, old_highest_id):
    new_highest_id = old_highest_id + 1
    self.fencer_id = "ID" + new_highest_id
    
    self.name = name

    return new_highest_id

class Poule:
  pass

class Round:
  '''
  Essentially one "week" of an event, consisting of fencers and poules. All of the "thinking" (analysing of raw data from a Poule) happens here, as it can also access the Fencer objects
  
  Attributes:
    + dict: metadata
    + Fencer[]: fencers
    + Poule[]: poules
  Methods:
    + boolean: parse_data() # extracts and calculates data (w, l, hr, hg, ind) for each fencer
  '''
  # TODO: Should fencers be here or in year? Should be easy enough to change, just pass in fencers to input. But, do I want changes to fencers here to affect fencers globally?
  def __init__(self, prev_rankings):
    ''' Input: prev_rankings - list of fencers, sorted in descending order (i.e. best to worst), from the previous round '''
    pass

  def 

# Will need to pass in the list of fencers to the child for fencer ids. pass by reference