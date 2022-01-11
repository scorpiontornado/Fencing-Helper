def allocate_poules(rankings, num_pools):

  # for 3 poules: 0 1 2 2 1 0 0 1 2 2 1 0
  
  # Poules of 6 or 7 if possible for formal comps. 
  #poules = [[]*num_pools]
  poules = [[] for _ in range(num_pools)] # Create empty poules
  print(poules)

  index_from = 0
  index_to = 0 # Poule index_to put the fencer in
  direction = 1 # +1 for forwards, -1 for backwards. The number index_to is incremented by.
  
  while index_from < len(rankings):
    #print("Start", index_to, poules[index_to], direction)
    print(f"index_to: {index_to}, poules: {poules}, poules[index_to]: {poules[index_to]}, direction: {direction}")
    #print("Middle", index_to, poules[index_to], direction, len(poules) - 1)

    poules[index_to].append(rankings[index_from])
    if index_to >= len(poules) - 1:
      # change direction if above upper boundary, and put it back at the boundary
      #index_to = len(poules) - 1
      direction = -1
      print("Now going down")
      index_from += 1
      if index_from != len(rankings) - 1 :
        poules[index_to].append(rankings[index_from+1]) # TODO: make it work without this sloppy workaround
      
    elif index_to <= 0 and poules[0] != rankings[index_from]:
      # The and clause prevents it from being run at the beginning.
      # change direction if below lower boundary, and put it back at the boundary
      #index_to = 0 
      
      direction = 1
      print("Now going up")
      index_from += 1
      if index_from != len(rankings) - 1 :
        # Only run if not the last fencer
        poules[index_to].append(rankings[index_from+1]) # TODO

    index_from += 1
    index_to += direction # increment index_to by direction
    #print("End", index_to, poules[index_to], direction)

  return poules

print(allocate_poules([1,2,3,4,5,6], 3))
print(allocate_poules([1,2,3,4,5,6,7,8,9,10,11,12], 5))