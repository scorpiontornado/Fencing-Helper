# For the moment, all setup and input happens here. I might modularise/abstract this later.
import scoresheet
import re

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

def swap(arguments, cur_event, cur_round, round_num, cur_poule, poule_num):
  if len(arguments) != 2:
    print("Invalid number of arguments")
    
  elif arguments[0] in ("poule", "poules") and int(arguments[1]) >= 1 and int(arguments[1]) <= len(cur_round.poules):
    poule_num = int(arguments[1])
    cur_poule = cur_round.poules[poule_num-1]

    print(f"\n ######### ROUND {round_num} #########")
    cur_round.display_poules(poule_num)  
    cur_poule.display_raw_data() # display the raw data (scores)
    
  elif arguments[0] in ("round", "rounds") and int(arguments[1]) >= 1 and int(arguments[1]) <= len(cur_event.rounds):
    round_num = int(arguments[1])
    cur_round = cur_event.rounds[round_num-1]

    poule_num = 1
    cur_poule = cur_round.poules[0]

    print(f"\n ######### ROUND {round_num} #########")
    cur_round.display_poules()
    
  else:
    print("Invalid argument(s)")

  return cur_round, round_num, cur_poule, poule_num

def score(arguments, cur_poule):
  if len(arguments) == 4:
    fencer_id1, score1, fencer_id2, score2 = arguments # set variables
    # TODO: a way to do this that is easier for the user than having to use fencer_ids. Maybe indexes?

    # Strip scores of non-numeric characters using regex
    # https://stackoverflow.com/questions/1450897/remove-characters-except-digits-from-string-using-python#comment103764679_1450900
    score1 = int(re.sub(r"\D+", "", score1)) # \D matches any non-digit character # TODO: store as int or string?
    score2 = int(re.sub(r"\D+", "", score2)) # \D matches any non-digit character
    print("score1:", score1, score2)

    cur_poule.input_scores(fencer_id1, score1, fencer_id2, score2) # input the scores
    cur_poule.display_raw_data() # display the raw data (scores)

  else:
    print("Invalid number of arugments.")

def process(arguments, cur_round):
  cur_round.process_data()
  cur_round.generate_rankings()
  cur_round.display_results()
  # print(cur_round.unranked_results) # for testing

def create(arguments, cur_round, round_num, cur_poule, poule_num):
  if len(arguments) != 1:
    print("Invalid number of arguments")
  
  elif arguments and arguments[0] == "round":
    # PROCESS DATA (if not already done)
    if not hasattr(cur_round, "ranked_results"):
      cur_round.process_data()
      cur_round.generate_rankings()
    id_rankings = list(cur_round.ranked_results.keys()) # Get sorted list of fencer ids
    #print(id_rankings)
    print(f"\n ######### RESULTS FOR CURRENT ROUND #########")
    cur_round.display_results()

    date = "" if len(arguments) == 1 else arguments[1] # TODO: auto-set date
    
    cur_round = cur_event.new_round({"date":date}, id_rankings = id_rankings)
    round_num = len(cur_event.rounds)
    
    cur_round.allocate_poules()
    print(f"\n ######### ROUND {round_num} #########")
    cur_round.display_poules()
    
    poule_num = 1
    cur_poule = cur_round.poules[0]
  
  else:
    print("Invalid argument")

  return cur_round, round_num, cur_poule, poule_num

### INITIALISE DUMMY EVENT ###
years = {} # The highest-level data structure.

# TODO: create an input system (maybe from a file?) to automatically add events like "2022 Jan-Mar U14 epee individual event"
# TODO: create a backup system so that event data isn't lost on program restart - pickle

years["2022"] = [scoresheet.Event({"months": "Jan-Mar", "school_years": "10-12", "weapon": "epee", "type": "individual"}, "name_rankings.txt")]

cur_event = years["2022"][-1]

for fencer in cur_event.fencers:
  print(fencer)

cur_round = cur_event.new_round({"date":"20220111"})
round_num = 1
cur_round.allocate_poules()
print(f"\n ######### ROUND {round_num} #########")
cur_round.display_poules()

cur_poule = cur_round.poules[0]
poule_num = 1

cur_poule.raw_data = [
  ["X", 5, 4, 5, 2, 5],
  [1, "X", 3, 5, 2, 3],
  [5, 5, "X", 4, 3, 5],
  [2, 4, 5, "X", 3, 4],
  [5, 5, 5, 5, "X", 5],
  [4, 5, 4, 5, 3, "X"],
] # debugging
cur_poule.display_raw_data() # display the raw data (scores)

### UI ###
user_input = input("\n\nWhat would you like to do? (You can always type 'help'!) ")
while user_input:
  user_input = user_input.split()
  command = user_input[0].lower()
  arguments = user_input[1:]
  
  if command == "help":
    help(arguments)
  
  elif command in ("swap, switch"):
    cur_round, round_num, cur_poule, poule_num = swap(arguments, cur_event, cur_round, round_num, cur_poule, poule_num)
  
  elif command in ("score", "scores"):
    score(arguments, cur_poule)
      
  elif command in ("process", "rankings", "results"):
    process(arguments, cur_round)

  elif command in ("create", "new"):
    cur_round, round_num, cur_poule, poule_num = create(arguments, cur_round, round_num, cur_poule, poule_num)
  
  else:
    print("Command not recognised. Sorry!")
  
  user_input = input("\nWhat would you like to do? ")