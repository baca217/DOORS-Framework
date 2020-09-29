import Levenshtein

#shows number of transformations needed to create the same senetence
print(Levenshtein.distance('Levenshtein Distance', 'Levensthein Distance'))
#doesn't work for longer stuff
print(Levenshtein.distance('This is a foo bar sentence', 'This sentence is similar to a foo bar sentence'))
