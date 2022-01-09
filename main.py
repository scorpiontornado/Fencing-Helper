

'''
data structure

years = {
  "2019": events
  "2020": events
  "2021": events
}

events = [
  {
    school_years: "10-12",
    rounds: [
      Round object
        metadata = {dates: Datetime object}
        fencers = [
          Fencer object
            fencer_id ("ID" + integer, e.g. "ID25" "ID1")
            name
            data = {wins, losses, HR, HG, ind} # could be an object (unecessary)
        ]
        poules = [
          Poule object
            key (list of fencer ids)
            raw_data (basically user input into scorecard)
        ]
    ]
  }
]


NOTE: the index of the fencer ids in keys corresponds to the index of rows & columsn of raw_data - so basically a parallel list


todo: incorporate the two, or split it up into sub sections.
note: age_brackets changed to categories and then to events
"ages" changed to "school_years" (as SACS groups events by school year). Might change back to "ages" if used in interschool - they group by U14, U16, U19.
'''

