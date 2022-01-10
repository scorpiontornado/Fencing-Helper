import scoresheet

years = {}

years["2022"] = scoresheet.Event({"school_years": "10-12", "weapon": "epee", "type": "individual"}, "name_rankings.txt")

for fencer in years["2022"].fencers:
  print(fencer, fencer.fencer_id, sep="   ")

# Testing if you can multiply a string by 0
print("\n" + "hi"*2 + "hello"*0 + "goodbye") # yes you can, hello never appears

# Testing
def generate_id(highest_id):
  # Number of 0s to pad with
  padding = 3 - len(str(highest_id))
  if padding < 0: padding = 0 # padding is 0 minimum, if the number of digits is 3 or more. E.g. "ID2063"

  return "ID" + "0"*padding + str(highest_id)


print(f"\n{generate_id(1)} {generate_id(10)} {generate_id(100)} {generate_id(1000)} {generate_id(10000)} {generate_id(2063)}")
# Output: ID001 ID010 ID100 ID1000 ID10000 ID2063