import pickle # serialisation and de-serialisation
from commands import help, switch, score, display, create
from setup import create_league, display_initial_data

###

# Attempt to de-serialse & load years from "years.pickle"
try:
  with open("league.pickle", "rb") as file:
    league = pickle.load(file) # de-serialise & load data contained in file "league.pickle" and assign to league
    
except (FileNotFoundError, EOFError):
  league = create_league()

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
    score(arguments, league.current) # input raw data (the final score of a single bout) to current poule

  elif command == "display":
    display(arguments, league.current) # generate and display fencer rankings for current round

  elif command in ("create", "new"):
    create(arguments, league.current) # create a new round or event object and update LEAGUE.CURRENT
  
  else:
    print("Command not recognised. Sorry!")

  # Serialise object and store in "years.pickle"
  with open("league.pickle", "wb") as file:
    pickle.dump(league, file, protocol=pickle.HIGHEST_PROTOCOL)
    # print("\nDumped league to pickle\n")
  
  user_input = input("\nWhat would you like to do? ")