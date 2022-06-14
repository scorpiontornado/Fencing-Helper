# TODO: run tests based on dummy data from testing_data.txt
# put in appendix w/ test data

import pickle # serialisation and de-serialisation
from commands import help, switch, score, process, create
from setup import create_league, display_initial_data

###

# Attempt to de-serialse & load years from "years.pickle"
try:
  with open("league.pickle", "rb") as file:
    # TODO: write description of years, similar to the one I did for the (now deprecated) years
    league = pickle.load(file) # de-serialise & load data contained in file "league.pickle" and assign to league
    # print("Successfully loaded league.pickle\n")
    
except (FileNotFoundError, EOFError):
  print("league.pickle not found, creating a new league")
  league = create_league()
  print("Successfully created new league\n")

###

display_initial_data(league)

### UI ###
user_input = input("\n\nWhat would you like to do? (You can always type 'help'!) ")
while user_input:
  user_input = user_input.split()
  command = user_input[0].lower()
  arguments = user_input[1:]
  
  if command == "help":
    help(arguments) # list commands the user can perform with example usages
  
  elif command in ("switch", "swap"):
    # TODO: Change to switch?
    switch(arguments, league.current) # modifies the LEAGUE.CURRENT dictionary, switching the current round or poule
  
  elif command in ("score", "scores"):
    score(arguments, league.current)

  # This command is now obsolete
  elif command in ("process", "rankings", "results"):
    process(arguments, league.current)

  elif command in ("create", "new"):
    league.current = create(arguments, league.current)
  
  else:
    print("Command not recognised. Sorry!")

  # Serialise object and store in "years.pickle"
  with open("league.pickle", "wb") as file:
    pickle.dump(league, file, protocol=pickle.HIGHEST_PROTOCOL)
    # print("\nDumped league to pickle\n")
  
  user_input = input("\nWhat would you like to do? ")