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
cur_round.display_poule()