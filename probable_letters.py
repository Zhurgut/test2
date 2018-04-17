# Here future Camenisch shall devise program to determine which letters
# are more likely than others, using the words.txt list
thing = open('words.txt')
nr_of_words = len(thing.readlines)
thing.close

print(nr_of_words)
