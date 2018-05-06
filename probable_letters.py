# Here future Camenisch shall devise program to determine which letters
# are more likely than others, using the words.txt list
print("imported probable letters")

alphabet = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l",
    "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
    ]

list_of_possibles = []

def make_list_of_possibles_len(length):
    # makes a list based of the length of the word that was chosen
    new_length = length + 1
    with open("C:\words.txt") as dict:
        word = dict.readline()
        while len(word) > 0:
            if len(word) == new_length:
                list_of_possibles.append(word.lower())
            word = dict.readline()
    for nr in range(len(list_of_possibles)):
        list_of_possibles[nr] = list_of_possibles[nr][:-1]
    return list_of_possibles


# make_list_of_possibles_len(8)


def give_index_of_nth_biggest(listt, nth):
    listing = []
    for elem in listt:
        listing.append(elem)
    new_list = []
    big = 0
    small = 5000000
    for elem in listing:
        if elem > big:
            big = elem
        if elem < small:
            small = elem
    new_list.append(small)
    new_list.append(big)
    for elem in listing:
        if elem == small or elem == big:
            listing.remove(elem)
    for elem in listing:
        ind = 1
        for nr in range(len(listt)):
            if elem >= new_list[ind - 1] and elem <= new_list[ind]:
                new_list.insert(ind, elem)
                break
            else:
                ind += 1
    new_list = new_list[::-1]
    wanted = new_list[nth]
    for nr in range(len(listt)):
        if wanted == listt[nr]:
            return nr
            break


def nth_likely_letter(wordlist, n):
    list_of_counts = []
    for letter in alphabet:
        count = 0
        for nr in range(len(list_of_possibles)):
            if letter in list_of_possibles[nr]:
                count += 1
        list_of_counts.append(count)
    br = give_index_of_nth_biggest(list_of_counts, n)
    return alphabet[br]
