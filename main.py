import scoresheet

years = {}

years["2022"] = scoresheet.Event({"school_years": "10-12", "weapon": "epee", "type": "individual"}, "name_rankings.txt")

print(years["2022"].name_rankings)