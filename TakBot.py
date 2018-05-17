# I shall yet play that fucken game!


# We have a board.
# We'll define a generator, which will return all possible boardpositions after one move.
# We'll define a function, which can evaluate, if a certain boardposition is won or lost resp.
# We'll have to define functions, which alter the board by making a move and find a way to interate through all possible such alterations
#
# We take a board as input.
# our generator will then spit out all possible board positions after one move
# we check if any of those positions is won, if it is, return that move (so we go through the whole generator once)
# now we go through the generator again...
# this time, if the position is not lost, we check if there is any winning move for the opponent
# if there isnt, we yield that board position
# (which is a board that has undergone one move, and which is certain not to have a winning move for the opponent)
# now with all those positions, we check if there were a winning move, if it were again our turn.
# if there is indeed one, we return the first move.
# if there is no winning move even after to moves, we check again, if there is a winning move for the opponent
# for every board after one move
# and if there isnt, we simply return (so we don't pressure the opponent by checking him, but he can't win in the next move at least.)
# if there is no move which does prevent the opponent from having a winning move after that one, we can just as well resign.
# i think this works, it wont be able to think very far but yeah we'll see.
# 1 is the human (white), 2 the pc (black)
# white goes first


# config:

board_size = 5

# end of config


if board_size == 3:
    nr_of_stones = 10
    nr_of_capstones = 0
elif board_size == 4:
    nr_of_stones = 15
    nr_of_capstones = 0
elif board_size == 5:
    nr_of_stones = 21
    nr_of_capstones = 1
elif board_size == 6:
    nr_of_stones = 30
    nr_of_capstones = 1

board = {
    "turn": 0,
    "white_stones": nr_of_stones,
    "black_stones": nr_of_stones,
    "white_capstones": nr_of_capstones,
    "black_capstones": nr_of_capstones,
    "board": {}
}

letters = ["a", "b", "c", "d", "e", "f"]
letters = letters[:board_size]
numbers = []
directions = ["up", "down", "right", "left"]

for letter in letters:
    for nr in range(board_size):
        if str(nr) not in numbers:
            numbers.append(str(nr))
        board["board"][(letter, str(nr))] = []


def print_board():
    global board
    player = board["turn"] % 2 + 1
    max_length = 0
    for key in board["board"]:
        if len(board["board"][key]) > max_length:
            max_length = len(board["board"][key])
    max_length += 1
    print("turn nr: ", board["turn"])
    print("white_stones", board["white_stones"])
    print("black_stones", board["black_stones"])
    print("white_capstones", board["white_capstones"])
    print("black_capstones", board["black_capstones"])
    print("Next Player: ", player)
    line_list = []
    line_list.append(f"     0")
    for line in numbers[1:]:
        line_list.append(round(max_length * 5) * " " + f"{line}")
    print(line_list)
    for column in letters:
        col_list = []
        col_list.append(column)
        for line in numbers:
            col_list.append(board["board"][(column, line)])
            _ = ((max_length - len(board["board"][(column, line)])) * 3) * " "
            col_list.append(_)
        print(col_list)
        print()


def place(pos, what_stone):
    global board
    player = board["turn"] % 2 + 1
    stone = 0
    check = 0
    if pos in board["board"].keys():
        if board["board"][pos] == []:
            if what_stone == "normal":
                stone = str(player)
                if player == 1 and board["white_stones"] > 0:
                    board["white_stones"] -= 1
                elif player == 2 and board["black_stones"] > 0:
                    board["black_stones"] -= 1
                else:
                    check = 1
                    print("no more stones left")

            elif what_stone == "wall":
                stone = -1 * player
                if player == 1 and board["white_stones"] > 0:
                    board["white_stones"] -= 1
                elif player == 2 and board["black_stones"] > 0:
                    board["black_stones"] -= 1
                else:
                    check = 1
                    print("no more stones left")

            elif what_stone == "capstone":
                stone = str(10 * player)
                if player == 1 and board["white_capstones"] > 0:
                    board["white_capstones"] -= 1
                elif player == 2 and board["black_capstones"] > 0:
                    board["black_capstones"] -= 1
                else:
                    check = 1
                    print("no more stones left")

            if stone != 0 and check == 0:
                board["board"][pos].append(stone)
                board["turn"] += 1
                return board


def get_relevant_fields(pos, direction, drops):
    relevant_cords = []
    if direction == "up":
        dube = letters.index(pos[0])
        for letter in letters[dube - len(drops):dube]:
            relevant_cords.append((letter, pos[1]))
    elif direction == "down":
        dube = letters.index(pos[0]) + 1
        for letter in letters[dube:dube + len(drops)]:
            relevant_cords.append((letter, pos[1]))
    elif direction == "right":
        dube = numbers.index(pos[1]) + 1
        for nr in numbers[dube:dube + len(drops)]:
            relevant_cords.append((pos[0], nr))
    elif direction == "left":
        dube = numbers.index(pos[1])
        for nr in numbers[dube - len(drops):dube]:
            relevant_cords.append((pos[0], nr))
    return relevant_cords


def move(pos, direction, drops):
    global turns, board, board_size, letters, numbers, directions
    nr_of_stones_taken = sum(drops)
    player = board["turn"] % 2 + 1

    def get_relevant_fields_in_order():
        if direction == "up" or direction == "left":
            return get_relevant_fields(pos, direction, drops)[::-1]
        else:
            return get_relevant_fields(pos, direction, drops)

    def get_last_field_of_move():
        if direction == "up":
            last_field = (letters[letters.index(pos[0]) - len(drops)], pos[1])
        elif direction == "down":
            last_field = (letters[letters.index(pos[0]) + len(drops)], pos[1])
        elif direction == "right":
            last_field = (pos[0], numbers[numbers.index(pos[1]) + len(drops)])
        elif direction == "left":
            last_field = (pos[0], numbers[numbers.index(pos[1]) - len(drops)])
        return last_field

    def check_for_walls():
        nr_of_walls = 0
        spaces_with_walls = []
        relevant_walls = []
        rly_relevant_walls = []
        for space in board["board"]:
            if board["board"][space] != []:
                if int(board["board"][space][-1]) < 0:
                    nr_of_walls += 1
                    spaces_with_walls.append(space)
        if nr_of_walls > 0:
            if pos in spaces_with_walls:
                spaces_with_walls.remove(pos)

        if len(spaces_with_walls) > 0:
            for space in spaces_with_walls:
                if space[0] == pos[0] or space[1] == pos[1]:
                    relevant_walls.append(space)

        if len(relevant_walls) > 0:
            rly_relevant_fields = get_relevant_fields(pos, direction, drops)
            for wall in relevant_walls:
                if wall in rly_relevant_fields:
                    rly_relevant_walls.append(wall)

        if len(rly_relevant_walls) > 1:
            return False
        elif len(rly_relevant_walls) == 0:
            return True
        else:
            # now we've got one fucken wall in our way. here we determine, whether there is a capstone to crush it or not.
            if int(board["board"][pos][-1]) > 7 and drops[-1] == 1:  # its a capstone and there is a last drop of only the capstone
                if get_last_field_of_move() == rly_relevant_walls[0]:
                    return True
                else:
                    return False
            else:
                return False

    def check_for_capstone():
        relevant_fields = get_relevant_fields(pos, direction, drops)
        var = True
        for feld in relevant_fields:
            if board["board"][feld] != []:
                if int(board["board"][feld][-1]) > 7:
                    var = False
        return var

    a = pos in board["board"].keys()
    if a:
        aa = board["board"][pos] != []
        if aa:
            b = direction in directions
            if b:
                if direction == "up":
                    bb = pos[0] in letters[len(drops):]
                elif direction == "down":
                    bb = pos[0] in letters[:(board_size - len(drops))]
                elif direction == "right":
                    bb = pos[1] in numbers[:(board_size - len(drops))]
                elif direction == "left":
                    bb = pos[1] in numbers[len(drops):]

                if bb:
                    c = nr_of_stones_taken <= board_size
                    if c:
                        cc = len(board["board"][pos]) >= nr_of_stones_taken
                        if cc:
                            ccc = len(drops) < board_size
                            if ccc:
                                ad = abs(int(board["board"][pos][-1])) % 9
                                d = ad == player
                                if d:
                                    if check_for_capstone():
                                        if check_for_walls():
                                            condition = True
                                        else:
                                            condition = False
                                    else:
                                        condition = False
                                else:
                                    condition = False
                            else:
                                condition = False
                        else:
                            condition = False
                    else:
                        condition = False
                else:
                    condition = False
            else:
                condition = False
        else:
            condition = False
    else:
        condition = False

    if condition:
        stones_to_move = []
        for step in range(sum(drops)):
            stone = board["board"][pos].pop()
            stones_to_move.insert(0, stone)
        next_fields = get_relevant_fields_in_order()
        for step in range(len(drops)):
            for stones in range(drops[step]):
                board["board"][next_fields[step]].append(stones_to_move.pop(0))
        board["turn"] += 1
        return board


def is_won():
    global board
    player = board["turn"] % 2 + 1
    player = 3 - player
    stones_leftw = board["white_stones"] + board["white_capstones"]
    stones_leftb = board["black_stones"] + board["black_capstones"]

    def get_cap_pos():
        a = player == 1 and board["white_capstones"] == 1
        b = player == 2 and board["black_capstones"] == 1
        if a or b:
            return None
        else:
            for keys in board["board"].keys():
                if len(board["board"][keys]) > 0:
                    if int(board["board"][keys][-1]) == 10 * player:
                        return keys
                        break

    def get_road_pieces():
        results = []
        for keys in board["board"]:
            if len(board["board"][keys]) > 0:
                if int(board["board"][keys][-1]) == player or\
                        keys == get_cap_pos():
                    results.append(keys)
        return results

    def sort_and_find_road():
        posits = get_road_pieces()
        list_by_letters = []
        list_by_numbers = []
        for letter in letters:
            list_by_letters.append([])
            list_by_numbers.append([])

        def next_checker(points, ind_to_check, lischt):
            buffer_list = []
            if len(points) == 1:
                for elem in points:
                    points.remove(elem)
            elif len(points) > 1:
                for nr in range(len(points) - 1):
                    ind1 = lischt.index(points[nr][ind_to_check])
                    ind2 = lischt.index(points[nr + 1][ind_to_check])
                    if abs(ind1 - ind2) == 1:
                        elem1 = points[nr]
                        elem2 = points[nr + 1]
                        if elem1 not in buffer_list:
                            buffer_list.append(elem1)
                        if elem2 not in buffer_list:
                            buffer_list.append(elem2)
            delet_list = []
            for elem in points:
                if elem not in buffer_list:
                    delet_list.append(elem)
            for elem in delet_list:
                points.remove(elem)

        for nr in range(len(letters)):
            for point in posits:
                if point[0] == letters[nr]:
                    list_by_letters[nr].append(point)
                if point[1] == numbers[nr]:
                    list_by_numbers[nr].append(point)

        checker1 = 0
        checker2 = 0
        for lists in list_by_letters:
            if len(lists) == 0:
                checker1 = 1
                break
        for lists in list_by_numbers:
            if len(lists) == 0:
                checker2 = 1
                break

        if checker1 == 1 and checker2 == 1:
            return [[]]
        else:
            for lists in list_by_letters:
                next_checker(lists, 1, numbers)
            for lists in list_by_numbers:
                next_checker(lists, 0, letters)
            next_list = list_by_letters + list_by_numbers
            return next_list

    def get_groups(listt):
        if len(listt) < 2:
            list_with_groups = []
        else:
            list_with_groups = []
            for nr in range(len(listt) - 1):
                l_before = len(list_with_groups)
                list1 = listt[nr]
                for list2 in listt[nr + 1:]:
                    for point2 in list2:
                        for point1 in list1:
                            if point1 == point2:
                                next_group = list1 + list2
                                next_group = list(set(next_group))
                                if next_group not in list_with_groups:
                                    list_with_groups.append(next_group)
                l_after = len(list_with_groups)
                if l_before == l_after and list1 != []:
                    list_with_groups.append(list1)
            check = 0
            for points in listt[-1]:
                for lists in list_with_groups:
                    for poiiints in lists:
                        if poiiints == points:
                            check = 1
                            break
                    if check == 1:
                        break
                if check == 1:
                    break
            if check == 0 and listt[-1] != []:
                list_with_groups.append(listt[-1])
        for nr in range(1, len(list_with_groups)):
            if list_with_groups[nr] in list_with_groups[0]:
                list_with_groups.remove(list_with_groups[nr])
        return list_with_groups

    def is_road(lischht):
        for groups in lischht:
            top = 0
            bottom = 0
            right = 0
            left = 0
            for elem in groups:
                if elem[0] == "a":
                    top = 1
                elif elem[0] == letters[-1]:
                    bottom = 1
                elif elem[1] == "0":
                    left = 1
                elif elem[1] == numbers[-1]:
                    right = 1
            print("top bot lef rig", top, bottom, left, right)
            vert = top + bottom
            horiz = right + left
            print("cond for wall thing ", vert == 2 or horiz == 2)
            if vert == 2 or horiz == 2:
                return player
            else:
                print("there no road")
                return None

    def whohasmoretopstones():
        resultsw = []
        resultsb = []
        for keys in board["board"]:
            if len(board["board"][keys]) > 0:
                if int(board["board"][keys][-1]) == 1:
                    resultsw.append(keys)
                elif int(board["board"][keys][-1]) == 2:
                    resultsb.append(keys)
        if len(resultsw) > len(resultsb):
            return 1
        elif len(resultsw) < len(resultsb):
            return 2
        else:
            return None

    next_list = sort_and_find_road()

    while len(get_groups(next_list)) != 0 and\
            get_groups(next_list) != [[]] and\
            get_groups(next_list) != next_list:
        next_list = get_groups(next_list)
    print("list with groups :)))", next_list)

    condizio = True
    for keys in board["board"].keys():
        if board["board"][keys] == []:
            condizio = False
            break
    if board["turn"] < board_size * 2 - 1:
        print("too low turn")
        return None

    elif stones_leftw == 0 or stones_leftb == 0:
        print("Either no more stones")
        whohasmoretopstones()
    elif condizio:
        print("condizio")
        whohasmoretopstones()
    else:
        print("theres a road maybe?")
        is_road(next_list)


def get_human_move():
    print_board()
    inputt = input("p/m? ")
    while inputt != "p" and inputt != "m":
        inputt = input("p/m? ")
    if inputt == "p":
        abss = input("letter? ")
        while len(abss) < 1:
            abss = input("letter? ")
        bbs = input("number? ")
        while len(bbs) < 1:
            bbs = input("number? ")
        aabs = (abss, bbs)
        type = input("what type of stone? n/w/c ")
        while len(type) < 1:
            type = input("what type of stone? n/w/c ")
        if type == "n":
            type = "normal"
        elif type == "w":
            type = "wall"
        elif type == "c":
            type = "capstone"
        place(aabs, type)
    elif inputt == "m":
        abss = input("letter? ")
        while len(abss) < 1:
            abss = input("letter? ")
        bbs = input("number? ")
        while len(bbs) < 1:
            bbs = input("number? ")
        aabs = (abss, bbs)
        direct = input("direction? u/r/l/d ")
        while len(direct) < 1:
            direct = input("direction? u/r/l/d ")
        if direct == "u":
            direct = "up"
        elif direct == "r":
            direct = "right"
        elif direct == "l":
            direct = "left"
        elif direct == "d":
            direct = "down"
        dropp = []
        for nr in range(board_size):
            droplet = input(f"drop? 0-{board_size} ")
            while len(droplet) < 1:
                droplet = input(f"drop? 0-{board_size} ")
            droplet = int(droplet)
            if droplet > 0:
                dropp.append(droplet)
            else:
                break
        move(aabs, direct, dropp)


place(("c", "4"), "normal")
place(("a", "3"), "normal")
place(("b", "1"), "normal")
place(("c", "3"), "normal")
place(("b", "2"), "normal")
place(("d", "3"), "normal")
place(("c", "2"), "normal")
place(("e", "3"), "normal")
place(("a", "2"), "normal")
place(("e", "2"), "normal")
place(("b", "3"), "normal")
place(("b", "4"), "normal")
place(("a", "0"), "normal")

while True:
    get_human_move()
    print("""
    winner?
    """, print(is_won()))
