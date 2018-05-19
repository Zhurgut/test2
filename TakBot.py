import itertools as it
import copy
import random

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

board_size = 4
nr_before_normal = 15  # nr of turn before which the bot only places normal stones

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


def get_moves_list(max_length):
    final = []
    final.append([max_length])
    list_to_combine = []
    list_with_numbers = list(range(1, max_length))  # [1, 2, 3, 4, 5]
    length = len(list_with_numbers)
    for nr in range(1, length + 1):  # [1, 2, 3, 4, 5]
        for time in range(max_length // nr):
            list_to_combine.append(nr)
    # print(list_to_combine)
    list_to_permute = []
    for nr_of_moves in range(1, max_length + 1):
        combs = list(it.combinations(list_to_combine, nr_of_moves))
        combs = set(combs)
        # print(nr_of_moves, combs)
        for elem in combs:
            if sum(elem) <= max_length:
                list_to_permute.append(elem)
    # print(list_to_permute)
    new_list_to_permute = []
    for elem in list_to_permute:
        list_to_append_to_permute = []
        for nr in elem:
            list_to_append_to_permute.append(nr)
        new_list_to_permute.append(list_to_append_to_permute)
    # print(new_list_to_permute)

    for elem in new_list_to_permute:
        perms = it.permutations(elem)
        perms = set(perms)
        # print(list(perms))
        for perm in perms:
            pen_final = []
            for nr in perm:
                pen_final.append(nr)
            final.append(pen_final)
    return final


all_moves1 = [[1]]
all_moves2 = get_moves_list(2)
all_moves3 = get_moves_list(3)
all_moves4 = get_moves_list(4)
all_moves5 = get_moves_list(5)
all_moves6 = get_moves_list(6)

types = {"normal", "capstone", "wall"}


def print_board(boardd):
    player = boardd["turn"] % 2 + 1
    max_length = 0
    for key in boardd["board"]:
        if len(boardd["board"][key]) > max_length:
            max_length = len(boardd["board"][key])
    max_length += 1
    print("turn nr: ", boardd["turn"])
    print("white_stones", boardd["white_stones"])
    print("black_stones", boardd["black_stones"])
    print("white_capstones", boardd["white_capstones"])
    print("black_capstones", boardd["black_capstones"])
    print("Next Player: ", player)
    line_list = []
    line_list.append(f"     0")
    for line in numbers[1:]:
        line_list.append(round(max_length * 4) * " " + f"{line}")
    print(line_list)
    for column in letters:
        col_list = []
        col_list.append(column)
        for line in numbers:
            col_list.append(boardd["board"][(column, line)])
            _ = ((max_length - len(boardd["board"][(column, line)])) * 3) * " "
            col_list.append(_)
        print(col_list)
        print()

#
#
# initial stuff
#
#
# now come place and move
#
#


def place(board, pos, what_stone):
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


def move(board, pos, direction, drops):
    global turns, board_size, letters, numbers, directions
    nr_of_stones_taken = sum(drops)
    player = board["turn"] % 2 + 1

    def flatten_walls():
        for pos in board["board"]:
            if len(board["board"][pos]) > 1:
                if int(board["board"][pos][-1]) > 7 and\
                        int(board["board"][pos][-2]) < 0:
                    board["board"][pos][-2] = str(-1 * board["board"][pos][-2])
                    break

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
        # print("last field ", last_field)
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
                # print(
                #     "last move ",
                #     get_last_field_of_move(), rly_relevant_walls[0]
                # )
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
                    break
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
        flatten_walls()
        return board

#
#
#
# these were the alterations to the board
#
# now comes the check for win
#
#


def is_won(board):
    player = board["turn"] % 2 + 1
    player = 3 - player
    stones_leftw = board["white_stones"] + board["white_capstones"]
    stones_leftb = board["black_stones"] + board["black_capstones"]

    def get_cap_pos():
        a = player == 1 and board["white_capstones"] == 1
        b = player == 2 and board["black_capstones"] == 1
        if a or b:
            # print("get cap pos ", a or b)  # ####################################################################
            return None
        else:
            for keys in board["board"].keys():
                if len(board["board"][keys]) > 0:
                    if int(board["board"][keys][-1]) == 10 * player:
                        # print("got cap pos keys at ", keys)  # ####################################################################
                        return keys

    def get_road_pieces():
        results = []
        for keys in board["board"]:
            if len(board["board"][keys]) > 0:
                if int(board["board"][keys][-1]) == player:
                    results.append(keys)
                elif keys == get_cap_pos():
                    results.append(keys)
        return results

    def sort_and_find_road():
        posits = get_road_pieces()
        # print("posits ", posits)  # ####################################################################
        list_by_letters = []
        list_by_numbers = []
        for letter in letters:
            list_by_letters.append([])
            list_by_numbers.append([])

        def next_checker(points, ind_to_check, lischt):  # removes all elements from points which have no connections
            # print(f"running next checker with {points} {ind_to_check} {lischt}")  # ##################################################
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
            # print(f" points now = {points}")

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
            # print("list by nr/lt ", list_by_letters, list_by_numbers)  # ##########################################################
            return next_list

    def get_groups(listt):
        if len(listt) < 2:
            list_with_groups = listt
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

        # for nr in range(1, len(list_with_groups)):
        #     if list_with_groups[nr] in list_with_groups[0]:
        #         list_with_groups.remove(list_with_groups[nr])

        return list_with_groups

    def cleaner(lischte):
        end_list = []
        del_list = []
        for elem in lischte:
            if elem == []:
                del_list.append(elem)
        for elem in del_list:
            lischte.remove(elem)
        for lichte in lischte:
            split_group = []
            for nr in range(len(lichte) - 1):
                ind1 = letters.index(lichte[nr][0])
                ind2 = letters.index(lichte[nr + 1][0])
                if ind1 == ind2:
                    ind1 = numbers.index(lichte[nr][1])
                    ind2 = numbers.index(lichte[nr + 1][1])
                # print(f"{lichte[nr]}, {lichte[nr + 1]}, {ind1}, {ind2}")
                if abs(ind1 - ind2) == 1:
                    if lichte[nr] not in split_group:
                        split_group.append(lichte[nr])
                    if lichte[nr + 1] not in split_group:
                        split_group.append(lichte[nr + 1])
                else:
                    end_list.append(split_group)
                    split_group = []
            end_list.append(split_group)
        return end_list

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
            # print("top bot lef rig", top, bottom, left, right)  # ####################################################################
            vert = top + bottom
            horiz = right + left
            # print("cond for wall thing ", vert == 2 or horiz == 2, player)  # ########################################################
            if vert == 2 or horiz == 2:
                print("player won")
                return player
        print("there no road")   # ####################################################################
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
            print("white more stones")   # ####################################################################
            return 1
        elif len(resultsw) < len(resultsb):
            print("black more stones")   # ####################################################################
            return 2
        else:
            print("draw")   # ####################################################################
            return None

    next_list = sort_and_find_road()  # list_by letters + l_b_numbers
    next_list = cleaner(next_list)
    counter = 0

    while len(get_groups(next_list)) != 0 and\
            get_groups(next_list) != [[]] and\
            get_groups(next_list) != next_list and\
            counter < 100:
        counter += 1
        next_list = get_groups(next_list)
        print("list with groups ", next_list)  # ####################################################################

    # print("B ", next_list)
    dl_list = []
    for nr in range(len(next_list) - 1):
        for point in next_list[nr]:
            for listt in next_list[nr + 1:]:
                for pointt in listt:
                    if point == pointt:
                        if len(next_list[nr]) >= len(listt):
                            if listt not in dl_list:
                                dl_list.append(listt)
                        elif len(next_list[nr]) < len(listt):
                            if next_list[nr] not in dl_list:
                                dl_list.append(next_list[nr])
                        break
    for elem in dl_list:
        next_list.remove(elem)
    # print("A ", next_list)

    print("list with groups :)))", next_list)  # our final fuckn lst argrg

    condizio = True
    for keys in board["board"].keys():
        if board["board"][keys] == []:
            condizio = False
            break
    if board["turn"] < board_size * 2 - 1:
        # print("too low turn")
        return None

    elif stones_leftw == 0 or stones_leftb == 0:
        print("Either no more stones")
        return whohasmoretopstones()
    elif condizio:
        print("condizio")
        return whohasmoretopstones()
    else:
        print("theres a road maybe?")
        return is_road(next_list)


#
# so now we know if won or not
#

# lets now make the generator for all moves
#
#
#
#

def get_all_moves(bret):
    bret1 = copy.deepcopy(bret)
    bret_before_move = copy.deepcopy(bret1)
    print_board(bret_before_move)
    # yields all possible board positions after one move without actually doing the move
    scrambled_keys = list(bret1["board"].keys())
    random.shuffle(scrambled_keys)
    for position in scrambled_keys:
        if bret1["board"][position] == []:
            # print("place() coming")  # #######################################################################
            # go through all possible place()
            for type in types:
                if bret_before_move["turn"] < nr_before_normal:  # at beginning only place normal stones
                    if type == "normal":
                        place(bret1, position, type)
                        # print_board(bret1)
                        # print(bret1["turn"], bret_before_move["turn"])
                        # print(bret1["turn"] > bret_before_move["turn"])
                        if bret1["turn"] > bret_before_move["turn"]:  # if a move was made
                            # print("move_was_made")
                            # print("before ")
                            # print_board(bret_before_move)
                            bret_after_move = copy.deepcopy(bret1)
                            # print("after ")
                            # print_board(bret_after_move)
                            bret1 = copy.deepcopy(bret_before_move)
                            # print_board(bret1)
                            print("placed")
                            yield bret_after_move
                else:
                    place(bret1, position, type)
                    # print_board(bret1)
                    # print(bret1["turn"], bret_before_move["turn"])
                    # print(bret1["turn"] > bret_before_move["turn"])
                    if bret1["turn"] > bret_before_move["turn"]:  # if a move was made
                        # print("move_was_made")
                        # print("before ")
                        # print_board(bret_before_move)
                        bret_after_move = copy.deepcopy(bret1)
                        # print("after ")
                        # print_board(bret_after_move)
                        bret1 = copy.deepcopy(bret_before_move)
                        # print_board(bret1)
                        print("placed")
                        yield bret_after_move
        else:
            # go through all possible move()
            # print("move coming !!!!!!!!!!!!!!!!")  # ##############################################################################
            max_len = board_size
            lennn = len(bret1["board"][position])
            if lennn < board_size:
                max_len = lennn
            if max_len == 1:
                drop_list = all_moves1
            elif max_len == 2:
                drop_list = all_moves2
            elif max_len == 3:
                drop_list = all_moves3
            elif max_len == 4:
                drop_list = all_moves4
            elif max_len == 5:
                drop_list = all_moves5
            elif max_len == 6:
                drop_list = all_moves6
            # print(drop_list)  # ##################################################################
            for direction in directions:
                for drop_pattern in drop_list:
                    bret_before_move = copy.deepcopy(bret1)
                    move(bret1, position, direction, drop_pattern)
                    if bret1["turn"] > bret_before_move["turn"]:  # if a move was made
                        bret_after_move = copy.deepcopy(bret1)
                        bret1 = copy.deepcopy(bret_before_move)
                        # print_board(bret1)
                        print("moved")
                        yield bret_after_move


#
#
#
#
#
# like that we get human move:
            #


def get_human_move():
    global board
    print_board(board)
    inputt = input("p/m? ")
    while inputt != "p" and inputt != "m":
        inputt = input("p/m? ")
    if inputt == "p":
        type = input("what type of stone? n/w/c ")
        while type not in ["n", "c", "w"]:
            type = input("what type of stone? n/w/c ")
        if type == "n":
            type = "normal"
        elif type == "w":
            type = "wall"
        elif type == "c":
            type = "capstone"
        abss = input("letter? ")
        while abss not in letters:
            abss = input("letter? ")
        bbs = input("number? ")
        while bbs not in numbers:
            bbs = input("number? ")
        aabs = (abss, bbs)
        place(board, aabs, type)
    elif inputt == "m":
        abss = input("letter? ")
        while abss not in letters:
            abss = input("letter? ")
        bbs = input("number? ")
        while bbs not in numbers:
            bbs = input("number? ")
        aabs = (abss, bbs)
        direct = input("direction? u/r/l/d ")
        while direct not in ["u", "r", "l", "d"]:
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
        move(board, aabs, direct, dropp)


#
# place(board, ("a", "0"), "normal")
# place(board, ("a", "1"), "normal")
#
# place(board, ("b", "1"), "normal")
# place(board, ("a", "3"), "normal")
#
# place(board, ("a", "2"), "normal")
# place(board, ("b", "0"), "normal")
#
# place(board, ("a", "4"), "normal")
# place(board, ("b", "2"), "normal")
#
# place(board, ("c", "1"), "normal")
# place(board, ("b", "3"), "normal")
#
# place(board, ("c", "3"), "normal")
# place(board, ("b", "4"), "normal")
#
# place(board, ("c", "4"), "normal")
# place(board, ("c", "0"), "normal")
#
# place(board, ("d", "2"), "normal")
# place(board, ("c", "2"), "normal")
#
# place(board, ("e", "0"), "normal")
# place(board, ("d", "0"), "normal")
#
# place(board, ("e", "2"), "normal")
# place(board, ("d", "1"), "normal")
#
# place(board, ("e", "4"), "normal")
# place(board, ("d", "3"), "normal")


winner = None

while is_won(board) is None and winner != 1:
    before_hum = copy.deepcopy(board)
    while board == before_hum:
        get_human_move()  # we get human move until a move was made
    winner = is_won(board)  # if white has won pc will make move but then
    # while loop will break
    if winner != 1:
        winning_move_made = 0
        for new_board in get_all_moves(board):
            if is_won(new_board) == 2:
                board = new_board
                winning_move_made = 1
                break  # if there is a winning move, break
        if winning_move_made == 0:          # no winning move was made, therefore go through loop again
            white_has_winning_move = 0
            for new_board in get_all_moves(board):                  #
                for board_after_white in get_all_moves(new_board):  # check if white has any winning moves after black move
                    if is_won(board_after_white) == 1:              #
                        white_has_winning_move = 1                  #
                        break
                if white_has_winning_move == 1:
                    break
            if white_has_winning_move == 1:
                print("white has a winning move")
                no_white_winning = []
                for new_board in get_all_moves(board):
                    white_has_winning_move_for_that_board = 0               #
                    for board_after_white in get_all_moves(new_board):  # for every new_board, check if white has no winning moves,
                        if is_won(board_after_white) == 1:                  #
                            white_has_winning_move_for_that_board = 1       #
                            break
                    if white_has_winning_move_for_that_board == 0:         # append new_board to list with all board where white can not win as soon as
                                                                            # found one move which has no winning moves for white
                        no_white_winning.append(new_board)
                for new_board in no_white_winning:
                    new_board["turn"] += 1
                    for board_after_black in get_all_moves(new_board):
                        if is_won(board_after_black) == 2:
                            new_board["turn"] -= 1
                            board = new_board                       # if a board where white cannot win has a possibility fo winning for black play it
                            winning_move_made = 1
                            break
                if winning_move_made == 0:
                    if len(no_white_winning) > 0:        # there are no new_board where neither black nor white can win
                        no_white_winning[0]["turn"] -= 1
                        board = no_white_winning[0]  # just move where white cant win
                else:
                    print(" I resign ")
            else:
                print("white has no winning moves... supposedly")  # if white has no winning moves: check for winning moves for black :)
                for new_board in get_all_moves(board):
                    new_board["turn"] += 1
                    for board_after_black in get_all_moves(new_board):  # for every new_board, if black has no winning moves,
                        if is_won(board_after_black) == 2:
                            new_board["turn"] -= 1
                            board = new_board                       # make move
                            winning_move_made = 1
                            break
                if winning_move_made == 0:                                   # if there arent any winning moves for anyone, no one cares *shrug*
                    board = next(get_all_moves(board))

print_board(board)
print(f"{is_won(board)} has won! gg ^^")
