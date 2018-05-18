import itertools as it

listing = [1, 3, 5, 4, 2, 6, 4, 9]
new_list = []
small = 100000
big = 0

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
    for nr in range(len(listing)):
        if elem >= new_list[ind - 1] and elem <= new_list[ind]:
            new_list.insert(ind, elem)
            break
        else:
            ind += 1

print(" a " in "bab")

listt = [["asd"], ["sc"], ["dw"], ["a"]]
for lists in listt:
    listt.remove(lists)

max_length = 1
final = []
final.append([max_length])
list_to_combine = []
list_with_numbers = list(range(1, max_length))  # [1, 2, 3, 4, 5]
length = len(list_with_numbers)
for nr in range(1, length + 1):  # [1, 2, 3, 4, 5]
    for time in range(max_length // nr):
        list_to_combine.append(nr)
print(list_to_combine)
list_to_permute = []
for nr_of_moves in range(1, max_length + 1):
    combs = list(it.combinations(list_to_combine, nr_of_moves))
    combs = set(combs)
    print(nr_of_moves, combs)
    for elem in combs:
        if sum(elem) <= max_length:
            list_to_permute.append(elem)
print(list_to_permute)
new_list_to_permute = []
for elem in list_to_permute:
    list_to_append_to_permute = []
    for nr in elem:
        list_to_append_to_permute.append(nr)
    new_list_to_permute.append(list_to_append_to_permute)
print(new_list_to_permute)

for elem in new_list_to_permute:
    perms = it.permutations(elem)
    perms = set(perms)
    print(list(perms))
    for perm in perms:
        pen_final = []
        for nr in perm:
            pen_final.append(nr)
        final.append(pen_final)

print(final)
