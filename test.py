def allocate_poules(rankings, num_poules):
  '''
  Allocate fencers to poules based on their rankings. Done in a manner that spreads out the top fencers as much as possible.

  For example, when inputted 12 fencers, it will place them in poules like so (where each sub-list is a poule, and each number is the fencer's rank):
    [[1, 10, 11], [2, 9, 12], [3, 8], [4, 7], [5, 6]]

  Inputs: rankings (fencer_ids in desc. order), num_poules (the number of poules to allocate fencers into)
  '''
  # TODO: come up with an algorithm / expression to determine num_poules. Ideally, you want there to be 6 or 7 fencers per poule in competition fencing
  # for 3 poules,  0 1 2 2 1 0 0 1 2 2 1 0
  
  # Poules of 6 or 7 if possible for formal comps. 
  #poules = [[]*num_poules]
  poules = [[] for _ in range(num_poules)] # Create empty poules
  print("Empty poules:", poules)
  print("Rankings:", rankings)

  index_from = 0
  index_to = 0 # Poule index_to put the fencer in
  direction = 1 # +1 for forwards, -1 for backwards. The number index_to is incremented by.

  while index_from < len(rankings):
    # 1. Assign fencer to poule
    poules[index_to].append(rankings[index_from])

    # 2. Increment index_from by 1
    index_from += 1
    
    # 3. Increment index_to by direction
    index_to += direction
    
    # 4. Check if index_to has gone over the boundaries, if so, reset to boundary and change direction
    # (Checking > rather than >= 0 ensures it won't be true on the first pass through, when index_to is 0)
    if index_to > num_poules - 1: # check uppper boundary
      index_to = num_poules - 1 # reset to upper boundary
      direction = -1 # go down
    elif index_to < 0: # check lower boundary
      index_to = 0 # reset to lower boundary
      direction = 1 # go up
    
  return poules # Returns for the sake of testing. When implemented properly, it will just create poule objects and assign the fencers to their keys

print("Output:", allocate_poules([1,2,3,4,5,6], 3), end="\n\n")
print("Output: ", allocate_poules([1,2,3,4,5,6,7,8,9,10,11,12], 5))