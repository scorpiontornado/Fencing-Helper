from scoresheet import League # custom class made by candidate

def load_bout_results(file_path, current):
  """
  Load raw data (bout results) for the first round from text file.
  File format:
    - Poules separated by an empty line ("\n\n")
    - Within each poule, grid-shaped format with values separated by commas, rows separated by newlines
  """

  with open(file_path) as f:
    raw_data = f.read()
  poules = raw_data.split("\n\n")

  # Loop over each poule
  for i, poule in enumerate(poules):
    temp = []
    
    # Loop over each row
    for row in poule.split():
      temp.append(row.split(",")) # Append all values in row to temp

    current["round"].poules[i].raw_data = temp    

def create_league():
  # TODO: create an input system (maybe from a file?) to automatically add events like "2022 Jan-Mar U14 epee individual event". Or, add a setup process with user input, e.g. "Welcome to Fencing Helper. Let's set up a new event." "When is "
  
  ### INITIALISE DUMMY LEAGUE & EVENT ###
  league = League() # the highest-level data structure.
  event_metadata = {"start_date": "2022-05-19", "end_date": "2022-06-19", "year_groups": "10-12", "weapon": "epee", "type": "individual"} # user-inputted. Currently dummy data
  league.new_event(event_metadata, "input_files/name_rankings.txt")
  
  # LEAGUE.CURRENT is a dictionary that stores references to the current event, round, and poule,
  # as well as the (1-indexed) integer indexes corresponding to the current round and poule for outputting purpose
  # (the current system is 1-indexed, i.e. "Poule 1" is the first poule, as it is more understandable for users)
  # Create new instance of Round object and assign to league.current["round"]
  round_metadata = {"date":"20220111"} # user-inputted. TODO: make sure create round accepts round data. # TODO: should this come from a file?
  league.current["round"] = league.current["event"].new_round(round_metadata)
  league.current["round_num"] = 1
  
  # Automatically allocate poules based on initial rankings in name_rankings.txt
  league.current["round"].allocate_poules()
  
  # Set the first poule to be the current poule in CURRENT
  league.current["poule"] = league.current["round"].poules[0]
  league.current["poule_num"] = 1

  # For testing functionality of program with predetermined raw data
  load_bout_results("input_files/raw_data.txt", league.current)

  return league

def display_initial_data(league):
  # Output the fencers in the current event to allow coaches to ensure no inputting errors have been made
  print("List of fencers in current event:\n")
  for fencer in league.current["event"].fencers:
    print(fencer)
  
  # Output all the poule lists (showing which fencers are in which poules) for the current round
  league.display_current(round_num=True, poule_num=False)
  league.current["round"].display_poules()
  
  # Output the raw data (scores) for the current poule
  league.display_current()
  league.current["poule"].display_raw_data()