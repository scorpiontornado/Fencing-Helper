class Poule:
  '''
  A poule is a group of fencers that verse each other in a round-robin type format, where each fencer bouts every other fencer once.

  For the MVP, inputs will ideally happen like this:
    input ID001 0, ID002 5
  or
    input ID004 V5 ID003 D2
  (All non-numerical digits are ignored in the 3rd and 5th "words")

  Attributes:
    + fencer_ids:String[] (array of fencer ids, i.e. "keys" - parallel to the rows/columns, used to find which fencer is at which row/column)
    + raw_data:String[][] (user input into scorecard). Rows signify the hits scored by the fencer against the people in the columns. E.g. using raw_data[row][column], raw_data[0][1] would be the number of times the fencer in index 0 hit the fencer in index 1. The main diagonal should remain empty.

  Methods:
    + init_raw_data()
    + get_index(fencer_id)
    + input_scores(fencer_id1, score1, fencer_id2, score2)
    + display_raw_data()
  '''
  def __init__(self):
    self.fencer_ids = [] # todo: some sort of failsafe if 0 fencers?

  def init_raw_data(self):
    '''
    Initialise the raw data (2-D array) with the correct number of rows and collumns, and populate the main diagonal with "X"s
    '''
    self.raw_data = [["_" for _ in range(len(self.fencer_ids))] for _ in range(len(self.fencer_ids))] # initialise empty scorecard with all values " "
    # initialise main diagonal with "X"s
    for i in range(len(self.fencer_ids)):
      self.raw_data[i][i] = "X"

  def get_index(self, fencer_id):
    '''
    Returns the index associated with the given fencer_id
    '''
    # Linear search
    for i, cur_id in enumerate(self.fencer_ids):
      if cur_id == fencer_id: return i

  def input_scores(self, fencer_id1, score1, fencer_id2, score2):
    '''
    Inputs the results of a bout / the scores of two fencers
    '''
    # TODO: should I allow index input instead of fencer ids?
    
    # Find the index of the inputted fencer ids
    index1 = self.get_index(fencer_id1) # Todo: have a failsafe if this returns None
    index2 = self.get_index(fencer_id2)
    # print(index1, index2)

    # check both ids are present in the poule
    # can't use "if index1 and index2" because index = 0 will == False
    if index1 != None and index2 != None:
      self.raw_data[index1][index2] = score1
      self.raw_data[index2][index1] = score2
    else:
      print("Invalid ID")

  def display_raw_data(self):
    '''
    WIP. Prints the raw data to the screen in a grid format.
    '''
    # Should this be called display_scores?
    #print(self.raw_data) # TODO: better print function

    # https://stackoverflow.com/questions/17870612/printing-a-two-dimensional-array-in-python
    print('\n'.join([''.join(['{:4}'.format(str(item)) for item in row]) 
      for row in self.raw_data]))

class Round:
  '''
  Essentially one "week" of an event, consisting of poules (groups of fencers). Assigns fencer (ids) to poules based on rankings, analyses the raw data from a poule
  
  Attributes:
    + metadata:dict
    + prev_id_ranks:String[]
    + num_poules:int
    + poules:Poule[]
    + unranked_results:dict
    + ranked_results:dict
    + new_id_ranks:String[]
  
  Methods:
    + allocate_poules(num_poules=None) (Allocates fencers into poules based on their rankings from the previous round)
    + display_poules(poule_num="all") (poule_num can be "all" (default) or any integer >= 0 and < self.num_poules)
    + process_data() (Extracts and calculates data (w, l, hg, hr, ind) for each fencer)
    + generate_rankings() (Ranks fencers in desc. order based on data from process_data)
    - dict_print(dict_) (Prints a given dictionary. Used in display_results)
    + display_results() (Displays the ranked results)
  
  # possibly TODO: make consistent. Rankings or results?
  '''
  # TODO: Should fencers be here or in year? Should be easy enough to change, just pass in fencers to input. But, do I want changes to fencers here to affect fencers globally?
  def __init__(self, parent, metadata, prev_id_ranks):
    ''' Input: metadata (dict with key "date"), rankings (list of fencers, sorted in desc. order (i.e. best to worst), from the previous round) '''
    self.parent = parent # Parent (Event) object
    
    self.metadata = metadata # TODO: should the date key be a string YYYYMMDD, DDMMYYYY, or a datetime object?
    self.prev_id_ranks = prev_id_ranks

  def allocate_poules(self, num_poules=None):
    '''
    Allocate fencers to poules based on their rankings. Done in a manner that spreads out the top fencers as much as possible.
  
    For example, when inputted 12 fencers, it will place them in poules like so (where each sub-list is a poule, and each number is the fencer's rank):
      [[1, 10, 11], [2, 9, 12], [3, 8], [4, 7], [5, 6]]

    Input: [num_poules] (must be an int, > 0 and <= len(self.prev_id_ranks))
    '''

    # TODO: determine num_poules automatically, but have some sort of override
    # Need to come up with an algorithm/expression to determine num_poules
    # Ideally, you want there to be 6 or 7 fencers per poule in competition fencing

    # TODO: allocate fencers to Poule objects rather than a 2-D list

    self.DEFAULT_NUM_FENCERS = 6 # the default number of fencers per poule. Usu. 6-7
    
    if (num_poules
        and isinstance(num_poules, int)
        and num_poules > 0
        and num_poules <= len(self.prev_id_ranks)):
          self.num_poules = num_poules # assign the number of poules manually
    else:
      self.num_poules = len(self.prev_id_ranks) // self.DEFAULT_NUM_FENCERS # auto-determine number of poules
    
    self.poules = [Poule() for _ in range(self.num_poules)] # Create empty poules
  
    index_from = 0
    index_to = 0 # Poule index_to put the fencer in
    direction = 1 # +1 for forwards, -1 for backwards. The number index_to is incremented by.
  
    while index_from < len(self.prev_id_ranks):
      # 1. Assign fencer to poule
      self.poules[index_to].fencer_ids.append(self.prev_id_ranks[index_from])
  
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

    # Initialise each poule
    for poule in self.poules:
      poule.init_raw_data()

  def display_poules(self, poule_num="all"):
    '''
    Displays the fencer ids in the given poule.
    Input: poule_num (can be "all" (default) or any integer >= 0 and < self.num_poules)
    '''
    if isinstance(poule_num, str) and poule_num.lower() == "all": # check to see if the user wants to display all poules. isinstance is necessary (to check that the input is a string) as integers dont have a .lower() method
      for i, cur_poule in enumerate(self.poules):
        print(f"\n ========= Poule {i+1} =========")
        for fencer_id in cur_poule.fencer_ids:
          fencer = self.parent.get_fencer_by_id(fencer_id)
          print(fencer) # TODO: put index next to fencer?
    elif isinstance(poule_num, int) and poule_num >= 0 and poule_num < self.num_poules:
      print(f"\n ========= Poule {poule_num} =========")
      for fencer_id in self.poules[poule_num-1].fencer_ids: # -1 because users will expect it to be 1-indexed rather than 0-indexed
        fencer = self.parent.get_fencer_by_id(fencer_id)
        print(fencer)
    else:
      print("Invalid poule number")

  def process_data(self):
    '''
    Processes (extracts & calculates) the data from raw data:
      v: number of victories
      m: number of matches (bouts) fenced in the poule by the particular fencer
      v/m: relative number of victories, v divided by m
      hg: hits gained (number of times you hit your opponent)
      hr: hits received (number of times you are hit by your opponent)
      ind: indicator, hg minus hr (hg-hr) (the higher the better)
    
    Creates one property:
      self.unranked_results: processed, unranked results (i.e. dictionary of dictionaries containing v, m ... for each fencer_id)
    '''
    # Loop through all fencers
    self.unranked_results = {}
    for poule in self.poules:
      for i, row in enumerate(poule.raw_data):
        # Note: fencer_ids[index] returns the fencer_id for the given index
        cur_fencer_id = poule.fencer_ids[i]
        self.unranked_results[cur_fencer_id] = {
          "v": 0,
          "m": 0,
          "hg": 0,
          "hr": 0,
        } # initialise dictionary for current fencer_id (note that v/b and ind are set later)
        
        # Loop over all opponents for the current fencer
        for j, value in enumerate(row):
          if (i == j
              or not isinstance(poule.raw_data[i][j], int)
              or not isinstance(poule.raw_data[j][i], int)):
            # If on main diagonal or if the position is not an integer (e.g. "_")
            # FIXME: i == j is redundant because the main diagonal should contain "X"s anyway... but I'm too scared to delete it
            continue

          self.unranked_results[cur_fencer_id]["m"] += 1 # Increment number of bouts fenced
          # Check wins
          if poule.raw_data[i][j] > poule.raw_data[j][i]:
             self.unranked_results[cur_fencer_id]["v"] += 1

          # hits gained
          # print(i, j, "poule.raw_data[i][j]", poule.raw_data[i][j])
          self.unranked_results[cur_fencer_id]["hg"] += poule.raw_data[i][j]
          
          # hits received
          self.unranked_results[cur_fencer_id]["hr"] += poule.raw_data[j][i]
          
        # relative bouts
        if self.unranked_results[cur_fencer_id]["m"] == 0:
          self.unranked_results[cur_fencer_id]["v/m"] = 0 # Avoid dividing by zero
        else:
          self.unranked_results[cur_fencer_id]["v/m"] = self.unranked_results[cur_fencer_id]["v"] / self.unranked_results[cur_fencer_id]["m"]  
        # indicator
        self.unranked_results[cur_fencer_id]["ind"] = self.unranked_results[cur_fencer_id]["hg"] - self.unranked_results[cur_fencer_id]["hr"]

  def generate_rankings(self):
    '''
    Creates two properties using self.unranked_results (from self.process_data()):
      self.ranked_results: processed, ranked results (sorted dictionary of dictionaries). For displaying round results
      self.new_id_ranks: sorted list of fencer_ids. For creating the next round's poules.
    '''

    self.new_id_ranks = sorted(self.unranked_results, key = lambda fid: (self.unranked_results[fid].get("v/m", 0), self.unranked_results[fid].get("ind", 0), self.unranked_results[fid].get("hg", 0)), reverse = True) # list of sorted keys (fencer_ids), sorted first by v/m, then by ind, then by hg.
    self.ranked_results = {fid:self.unranked_results[fid] for fid in self.new_id_ranks}
    # TODO: ties. Get the fencers to fence again, do a coin toss, or display a T after the rank, e.g. "21T"

  def dict_print(self, dict_):
    ''' Prints a dictionary in a nicer way. Used in display_results and debugging. '''
    for key in dict_:
      print(f"{key}: {dict_[key]}")
    print()

  def display_results(self):
    ''' Displays the dictionary of ranked results'''
    self.dict_print(self.ranked_results)
    
class Fencer:
  '''
  A single fencer, containing data for the current round only

  Attributes:
    + fencer_id:String ("ID" + >=3 digit integer, e.g. "ID025")
    + name:String
  Methods:
    + __str__()
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
  Event: a competition for a specific weapon and age category consisting of several “seeding” rounds (used to determine initial rankings that are used to organise fencers in a direct elimination tableau) followed by “direct elimination” rounds (used to determine the final placings – see “direct elimination tableau”). 
  
  Each object represents a single event, such as "years 10-12" or "epee teams event" for "U14", stored within a dictionary of years. 

  Attributes:
    + event_data:dict of Strings 
    + fencers:Fencer[]
    + rounds:Round[]
    
  Methods:
    + generate_id()
    + new_round(metadata, id_rankings=[]):Round
    + get_fencer_by_id(fencer_id):Fencer
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
    
    Output: round object that was just created
    '''
    if id_rankings: self.id_rankings = id_rankings # override the current id rankings stored in the event if passed in a new set of id rankings
    print("self.id_rankings:", self.id_rankings)
    self.rounds.append(Round(self, metadata, self.id_rankings)) # create a new round

    return self.rounds[-1]

  def get_fencer_by_id(self, fencer_id):
    ''' Returns the fencer object associated with the given fencer_id '''
    # Linear search
    for fencer in self.fencers:
      if fencer.fencer_id == fencer_id: return fencer