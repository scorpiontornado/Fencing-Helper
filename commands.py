### COMMANDS ###
import re # regex

# TODO: add commands to display fencer lists and poule lists?

def help(arguments):
  if not arguments:  
    print("""Here is a list of commands you can do:
    help
    switch
    score
    process
    create
  Type "help [command]" to learn more about each command!""")
  elif arguments[0] == "score":
    print('Usage: "score [fencer_id1], [score1], [fencer_id2], [score2]"')
  else:
    print("Command not recognised. Sorry!")

def switch(arguments, current):
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
    current["poule"].display_raw_data() # display the raw data (scores)
    
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
  # Do I need arguments? Helps with a consistent interface
  current["round"].process_data()
  current["round"].generate_rankings()
  current["round"].display_results() # Testing

def create(arguments, current):
  # Todo: create new event?
  if len(arguments) != 1:
    print("Invalid number of arguments")
  # error
  elif arguments and arguments[0] == "round":
    # PROCESS DATA (if not already done)
    if not hasattr(current["round"], "ranked_results"):
      process(arguments, current)
    
    id_rankings = list(current["round"].ranked_results.keys()) # Get sorted list of fencer ids
    #print(id_rankings)
    print(f"\n ######### RESULTS FOR PREVIOUS ROUND #########")
    current["round"].display_results()

    date = "" if len(arguments) == 1 else arguments[1] # TODO: auto-set date
    
    current["round"] = current["event"].new_round({"date":date}, id_rankings = id_rankings)
    current["round_num"] = len(current["event"].rounds)
    
    current["round"].allocate_poules()
    print(f"\n ######### ROUND {current['round_num']} #########") # TODO: There must be a way to put this into display_poules
    current["round"].display_poules()
    
    current["poule"] = current["round"].poules[0]
    current["poule_num"] = 1
    
  else:
    print("Invalid argument(s)")

    # return current # unecessary (will modify original copy, as it is pass-by-reference)