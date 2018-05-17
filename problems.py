
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

print(listt)
