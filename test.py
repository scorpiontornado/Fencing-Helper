def allocate_poules(rankings, num_pools):

  # for 3 poules: 0 1 2 2 1 0 0 1 2 2 1 0
  
  # Poules of 6 or 7 if possible for formal comps. 
  #poules = [[]*num_pools]
  poules = [[] for _ in range(num_pools)] # Create empty poules
  print(poules)

  to = 0 # Poule to put the fencer in
  direction = 1 # +1 for forwards, -1 for backwards. The number to is incremented by.]\
  for i, fencer_id in enumerate(rankings):
    #print("Start", to, poules[to], direction)
    print(f"to: {to}, poules: {poules}, poules[to]: {poules[to]}, direction: {direction}")
    #print("Middle", to, poules[to], direction, len(poules) - 1)

    poules[to].append(fencer_id)
    if to >= len(poules) - 1:
      # change direction if above upper boundary, and put it back at the boundary
      #to = len(poules) - 1
      direction = -1
      print("Now going down")
      to += direction
      if i != len(rankings) - 1 :
        poules[to].append(rankings[i+1]) # TODO: make it work without this sloppy workaround
      
    elif to <= 0 and poules[0] != [fencer_id]:
      # The and clause prevents it from being run at the beginning.
      # change direction if below lower boundary, and put it back at the boundary
      #to = 0 
      
      direction = 1
      print("Now going up")
      to += direction
      if i != len(rankings) - 1 :
        # Only run if not the last fencer
        poules[to].append(rankings[i+1]) # TODO

    to += direction # increment to by direction
    #print("End", to, poules[to], direction)

  return poules

print(allocate_poules([1,2,3,4,5,6], 3))
print(allocate_poules([1,2,3,4,5,6,7,8,9,10,11,12], 5))