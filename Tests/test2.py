def dict_print(dict_):
  for key in dict_:
    print(f"{key}: {dict_[key]}")
  print()

unranked_results = {'ID001': {'v': 3, 'm': 5, 'hg': 21, 'hr': 17, 'v/m': 0.6, 'ind': 4}, 'ID008': {'v': 1, 'm': 5, 'hg': 14, 'hr': 24, 'v/m': 0.2, 'ind': -10}, 'ID009': {'v': 3, 'm': 5, 'hg': 22, 'hr': 21, 'v/m': 0.6, 'ind': 1}, 'ID016': {'v': 1, 'm': 5, 'hg': 18, 'hr': 24, 'v/m': 0.2, 'ind': -6}, 'ID017': {'v': 5, 'm': 5, 'hg': 25, 'hr': 13, 'v/m': 1.0, 'ind': 12}, 'ID024': {'v': 2, 'm': 5, 'hg': 21, 'hr': 22, 'v/m': 0.4, 'ind': -1}, 'ID002': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID007': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID010': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID015': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID018': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID023': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID003': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID006': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID011': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID014': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID019': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID022': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID004': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID005': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID012': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID013': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID020': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}, 'ID021': {'v': 0, 'm': 0, 'hg': 0, 'hr': 0, 'v/m': 0, 'ind': 0}}

dict_print(unranked_results)

#id_rankings = sorted(unranked_results, key = lambda x: (unranked_results[x["v/m"]], unranked_results[x["ind"]], unranked_results[x["hg"]])) # list of sorted keys
id_rankings = sorted(unranked_results, key = lambda fid: (unranked_results[fid].get("v/m", 0), unranked_results[fid].get("ind", 0), unranked_results[fid].get("hg", 0)), reverse = True) # list of sorted keys (fencer_ids), sorted first by v/m, then by ind, then by hg.
ranked_results = {fid:unranked_results[fid] for fid in id_rankings}
# TODO: ties. Get the fencers to fence again, do a coin toss, or display a T after the rank, e.g. "21T"
print(id_rankings)
print()
dict_print(ranked_results)