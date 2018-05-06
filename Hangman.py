# I will do it, i will create a Hangman Program (which hopefully is not
# super slow)

import probable_letters as pl

list_of_possibles = pl.list_of_possibles

# length = 16
length = input("How long is your word, hein? ")
length = int(length)

print("Hmmm, lemme think")

pl.make_list_of_possibles_len(length)


current_known = []
current_k_string = []
for nr in range(length):
    current_known.append("[ ] ")
    current_k_string.append(" ")

asked = ""


def get_current_as_string():
    global current_k_string
    string = ""
    for letter in current_k_string:
        string += letter
    return string


def comparer():
    for elem in list_of_possibles:
        for ind in range(length):
            if get_current_as_string()[ind] != " ":
                if get_current_as_string()[ind] != elem[ind]:
                    list_of_possibles.remove(elem)



def print_known():
    stringi = ""
    for elem in current_known:
        stringi += elem
    print(stringi)
    indis = ""
    for nr in range(length):
        if length < 10:
            indis += f" {nr + 1}  "
        else:
            if nr < 9:
                indis += f" {nr + 1}  "
            else:
                indis += f" {nr + 1} "
    print(indis)


nr_of_wrong_guesses = 0


def print_hangman(nr_of_wrong_guesses):
    if nr_of_wrong_guesses == 0:
        pass
    elif nr_of_wrong_guesses == 1:
        print("""
        _____
        O    |
             |
             |
          ___|___
          """)
    elif nr_of_wrong_guesses == 2:
        print("""
        _____
        O    |
        |    |
             |
          ___|___
          """)
    elif nr_of_wrong_guesses == 3:
        print("""
        _____
        O__  |
        |    |
             |
          ___|___
          """)
    elif nr_of_wrong_guesses == 4:
        print("""
        _____
      __O__  |
        |    |
             |
          ___|___
           """)
    elif nr_of_wrong_guesses == 5:
        print("""
        _____
      __O__  |
        |    |
       /     |
          ___|___
          """)
    elif nr_of_wrong_guesses == 6:
        print("""
        _____
      __O__  |
        |    |
       / \   |
          ___|___

          You win, I hang""")



firstg = pl.nth_likely_letter(list_of_possibles, 0)
print(f"""Given that your word is {length} characters long, my first guess is '{firstg}'""")


def get_next_letter():
    n = 0
    for nr in range(26):
        next = pl.nth_likely_letter(list_of_possibles, n)
        if next in asked:
            n += 1
        else:
            return next
            break



    #determine next likely letter (inkl checking whether its in asked)



def ask_and_do(letter):
    global asked, nr_of_wrong_guesses, list_of_possibles
    # asks for the input, updates asked and updates current_known
    print_known()
    guess_pos = input(f"""Is '{letter}' in your word? If so, at what position?
    Please type '0' if '{letter}' is not in your word: """)
    guess_pos = int(guess_pos)
    asked += letter
    if guess_pos == 0:
        print("shit")
        nr_of_wrong_guesses += 1
        print_hangman(nr_of_wrong_guesses)
        for elem in list_of_possibles:
            if letter in elem:
                list_of_possibles.remove(elem)
    else:
        list_of_ind_to_change = []
        list_of_ind_to_change.append(guess_pos)
        for nr in range(length):
            guess_pos2 = input(f"""Does '{letter}' also appear in an other
            position? Type '0' if it doesn't. """)
            guess_pos2 = int(guess_pos2)
            if guess_pos2 != 0:
                list_of_ind_to_change.append(guess_pos2)
            else:
                break
        for pos in list_of_ind_to_change:
            pos -= 1
            current_known[pos] = f"[{letter}] "
            current_k_string[pos] = letter
    comparer()


ask_and_do(firstg)

print(list_of_possibles)
print(get_current_as_string())

while nr_of_wrong_guesses < 6:
    ask_and_do(get_next_letter())

print(list_of_possibles)

# guess1_pos = int(guess1_pos)
# asked += firstg
# if guess1_pos == 0:
#     nr_of_wrong_guesses += 1
#     print_hangman(nr_of_wrong_guesses)
# else:
#





#
# print(pl.list_of_possibles)
