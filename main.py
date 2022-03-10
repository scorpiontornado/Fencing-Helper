# For the moment, all setup and input happens here. I might modularise/abstract this later.

import scoresheet

years = {}

# TODO: create an input system (maybe from a file?) to automatically add events like "2022 Jan-Mar U14 epee individual event"
# TODO: create a backup system so that event data isn't lost on program restart

years["2022"] = [scoresheet.Event({"months": "Jan-Mar", "school_years": "10-12", "weapon": "epee", "type": "individual"}, "name_rankings.txt")]

for fencer in years["2022"][0].fencers:
  print(fencer)

years["2022"][0].new_round({"date":"20220111"})
cur_round = years["2022"][0].rounds[0] # TODO: should events.new_round() return the round?
cur_round.allocate_poules()
cur_round.display_poules()

# cur_round.display_poules(1) # working

poule_num = 1
poule = cur_round.poules[poule_num-1]
poule.display_raw_data() # display the raw data (scores)

user_input = input("\n\nWhat would you like to do? (You can always type 'help'!) ")
while user_input:
  user_input = user_input.split()
  command = user_input[0].lower()
  arguments = user_input[1:]
  
  if command == "help":
    if not arguments:  
      print("""Here is a list of commands you can do:
  help
  input
Type "help [command]" to learn more about each command!""")
    elif arguments[0] == "score":
      print('Usage: "score [fencer_id1], [score1], [fencer_id2], [score2]"')
    else:
      print("Command not recognised. Sorry!")
  
  elif command == "poule":
    poule_num = int(arguments[0])
    poule = cur_round.poules[poule_num-1]
  
  elif command == "score" or command == "scores":
    if len(arguments) == 4:
      fencer_id1, score1, fencer_id2, score2 = arguments # set variables
      # TODO: a way to do this that is easier for the user than having to use fencer_ids. Maybe indexes?
      # TODO: strip scores of non-numeric characters

      poule.input_scores(fencer_id1, score1, fencer_id2, score2) # input the scores
      poule.display_raw_data() # display the raw data (scores)

    else:
      print("Invalid number of arugments.")
  else:
    print("Command not recognised. Sorry!")
  
  user_input = input("\nWhat would you like to do? ")