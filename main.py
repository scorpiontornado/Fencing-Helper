import scoresheet

years = {}

# TODO: create an input system to automatically add events like "2022 Jan-Mar U14 epee individual event"

years["2022"] = [scoresheet.Event({"months": "Jan-Mar", "school_years": "10-12", "weapon": "epee", "type": "individual"}, "name_rankings.txt")]

for fencer in years["2022"][0].fencers:
  print(fencer)

# Testing
# def generate_id(highest_id):
#   # Number of 0s to pad with
#   padding = 3 - len(str(highest_id))
#   if padding < 0: padding = 0 # padding is 0 minimum, if the number of digits is 3 or more. E.g. "ID2063"

#   return "ID" + "0"*padding + str(highest_id)

# print(f"\n{generate_id(1)} {generate_id(10)} {generate_id(100)} {generate_id(1000)} {generate_id(10000)} {generate_id(2063)}")
# # Output: ID001 ID010 ID100 ID1000 ID10000 ID2063

years["2022"][0].new_round({"date":"20220111"})
