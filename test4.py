# Testing behaviour of objects in dictionaries

class Dog:
  def __init__(self, name):
    self.name = name

dog1 = Dog("Jack")
dog2 = Dog("Jill")

dogs = {"dog1": dog1, "dog2": dog2}

dogs["dog1"].name = "Jack the second"
dog2.name = "Jill the second"

print(dog1.name, dog2.name, dogs["dog1"].name, dogs["dog2"].name, sep="\n") # All print "[Jack/Jill] the second"
# Thus, objects stored in dictionaries, when modified, will modify everywhere
# I.e. dictionaries are pass-by-reference