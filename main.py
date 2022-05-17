# TODO: run tests based on dummy data from testing_data.txt
# put in appendix w/ test data

import scoresheet # custom classes made by candidate
import re # regex
import pickle # serialisation and de-serialisation

### COMMANDS ###
def help(arguments):
  if not arguments:  
    print("""Here is a list of commands you can do:
    help
    swap
    score
    process
    create
  Type "help [command]" to learn more about each command!""")
  elif arguments[0] == "score":
    print('Usage: "score [fencer_id1], [score1], [fencer_id2], [score2]"')
  else:
    print("Command not recognised. Sorry!")

def swap(arguments, current):
  if len(arguments) != 2:
    print("Invalid number of arguments")
    
  elif arguments[0] in ("poule", "poules") and int(arguments[1]) >= 1 and int(arguments[1]) <= len(current["round"].poules):
    current["poule_num"] = int(arguments[1])
    current["poule"] = current["round"].poules[current["poule_num"]-1]

    print(f"\n ######### ROUND {current['round_num']} #########")
    current["round"].display_poules(current["poule_num"])  
    current["poule"].display_raw_data() # display the raw data (scores)
    
  elif arguments[0] in ("round", "rounds") and int(arguments[1]) >= 1 and int(arguments[1]) <= len(current["event"].rounds):
    current["round_num"] = int(arguments[1])
    current["round"] = current["event"].rounds[current["round_num"]-1]

    current["poule_num"] = 1
    current["poule"] = current["round"].poules[0]

    print(f"\n ######### ROUND {current['round_num']} #########")
    current["round"].display_poules()
    
  else:
    print("Invalid argument(s)")
  
  # return current # unecessary (will modify original copy, as it is pass-by-reference)

def score(arguments, current):
  if len(arguments) == 4:
    fencer_id1, score1, fencer_id2, score2 = arguments # set variables
    # TODO: a way to do this that is easier for the user than having to use fencer_ids. Maybe indexes?

    # Strip scores of non-numeric characters using regex
    # https://stackoverflow.com/questions/1450897/remove-characters-except-digits-from-string-using-python#comment103764679_1450900
    score1 = int(re.sub(r"\D+", "", score1)) # \D matches any non-digit character # TODO: store as int or string?
    score2 = int(re.sub(r"\D+", "", score2)) # \D matches any non-digit character
    print("score1:", score1, score2)

    current["poule"].input_scores(fencer_id1, score1, fencer_id2, score2) # input the scores
    current["poule"].display_raw_data() # display the raw data (scores)

  else:
    print("Invalid number of arugments.")

def process(arguments, current):
  current["round"].process_data()
  current["round"].generate_rankings()
  current["round"].display_results()
  # print(current["round"].unranked_results) # for testing

def create(arguments, current):
  if len(arguments) != 1:
    print("Invalid number of arguments")
  
  elif arguments and arguments[0] == "round":
    # PROCESS DATA (if not already done)
    if not hasattr(current["round"], "ranked_results"):
      current["round"].process_data()
      current["round"].generate_rankings()
    id_rankings = list(current["round"].ranked_results.keys()) # Get sorted list of fencer ids
    #print(id_rankings)
    print(f"\n ######### RESULTS FOR CURRENT ROUND #########")
    current["round"].display_results()

    date = "" if len(arguments) == 1 else arguments[1] # TODO: auto-set date
    
    current["round"] = current["event"].new_round({"date":date}, id_rankings = id_rankings)
    current["round_num"] = len(current["event"].rounds)
    
    current["round"].allocate_poules()
    print(f"\n ######### ROUND {current['round_num']} #########")
    current["round"].display_poules()
    
    current["poule_num"] = 1
    current["poule"] = current["round"].poules[0]
  
  else:
    print("Invalid argument")

    # return current # unecessary (will modify original copy, as it is pass-by-reference)

# Attempt to de-serialse & load years from "years.pickle"
try:
  with open("league.pickle", "rb") as file:
    # TODO: write description of years, similar to the one I did for the (now deprecated) years
    league = pickle.load(file) # de-serialise & load data contained in file "league.pickle" and assign to league
    print("Successfully loaded league.pickle")
    print(league.current["poule_num"])
    
except (FileNotFoundError, EOFError):
  print("league.pickle not found, initialising league manually")
  # TODO: create an input system (maybe from a file?) to automatically add events like "2022 Jan-Mar U14 epee individual event"
  
  ### INITIALISE DUMMY LEAGUE & EVENT ###
  league = scoresheet.League() # the highest-level data structure.
  league.new_event({"months": "Jan-Mar", "school_years": "10-12", "weapon": "epee", "type": "individual"}, "name_rankings.txt")
  
  # Create new instance of Round object and assign to league.current["round"]
  league.current["round"] = league.current["event"].new_round({"date":"20220111"})
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

# Output the fencers in the current event to allow coaches to ensure no inputting errors have been made
for fencer in league.current["event"].fencers:
  print(fencer)

# Output the poule lists (showing which fencers are in which poules) for the current round
print(f"\n ######### ROUND {league.current['round_num']} #########")
league.current["round"].display_poules()

# Output the raw data (scores) for the current poule
league.current["poule"].display_raw_data()

# TODO: this overrites the file, so if you start and stop without inputting anything, it will lose all data.

### UI ###
user_input = input("\n\nWhat would you like to do? (You can always type 'help'!) ")
while user_input:
  user_input = user_input.split()
  command = user_input[0].lower()
  arguments = user_input[1:]
  
  if command == "help":
    help(arguments)
  
  elif command in ("swap, switch"):
    swap(arguments, league.current)
  
  elif command in ("score", "scores"):
    score(arguments, league.current)
      
  elif command in ("process", "rankings", "results"):
    process(arguments, league.current)

  elif command in ("create", "new"):
    league.current = create(arguments, league.current)
  
  else:
    print("Command not recognised. Sorry!")

  # Serialise object and store in "years.pickle"
  with open("league.pickle", "wb") as file:
    pickle.dump(league, file, protocol=pickle.HIGHEST_PROTOCOL)
    print("\nDumped league to pickle\n")
  
  user_input = input("\nWhat would you like to do? ")