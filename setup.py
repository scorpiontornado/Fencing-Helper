from scoresheet import League # custom class made by candidate

def create_league():
  # TODO: create an input system (maybe from a file?) to automatically add events like "2022 Jan-Mar U14 epee individual event"
  
  ### INITIALISE DUMMY LEAGUE & EVENT ###
  league = League() # the highest-level data structure.
  event_metadata = {"months": "Jan-Mar", "school_years": "10-12", "weapon": "epee", "type": "individual"} # user-inputted. Currently dummy data
  league.new_event(event_metadata, "name_rankings.txt")
  
  # LEAGUE.CURRENT is a dictionary that stores the current event, round, and poule, and the (1-indexed) index of the
  # current round and poule for outputting purposes (current system is 1-indexed -> more understandable for users)
  # Create new instance of Round object and assign to league.current["round"]
  round_metadata = {"date":"20220111"} # user-inputted. TODO: make sure create round accepts round data. # TODO: should this come from a file?
  league.current["round"] = league.current["event"].new_round(round_metadata)
  league.current["round_num"] = 1
  
  # Automatically allocate poules based on initial rankings in name_rankings.txt
  league.current["round"].allocate_poules()
  
  # Set the first poule to be the current poule in CURRENT
  league.current["poule"] = league.current["round"].poules[0]
  league.current["poule_num"] = 1
  
  # Insert dummy data. TODO: make it possible to do this via a file.
  league.current["poule"].raw_data = [
    ["X", 5, 4, 5, 2, 5],
    [1, "X", 3, 5, 2, 3],
    [5, 5, "X", 4, 3, 5],
    [2, 4, 5, "X", 3, 4],
    [5, 5, 5, 5, "X", 5],
    [4, 5, 4, 5, 3, "X"],
  ] # debugging

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