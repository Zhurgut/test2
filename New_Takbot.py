import itertools as it
import copy
import random

# config:

board_size = 4

# weights for value of board function:
# with these you can determine what the computer should focus more strongly on
super = 4       # nr of stones that count for a road
potent = 1      # nr of stones hidden in stacks of ones own controle
cappot = 2     # nr of stones hidden in a stack under the capstone
threat = 15     # nr of moves it takes to win

#################################################### stuff

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

types = ["normal", "capstone", "wall"]


# ################# Setting up the board

board = {
    "turn": 0,
    "white_stones": nr_of_stones,
    "black_stones": nr_of_stones,
    "white_capstones": nr_of_capstones,
    "black_capstones": nr_of_capstones,
    "board": {},
    "next_fields": {}
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

# ############################# setting up the various pick and move patters

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

# ###################################### setting up fields next to pos

all_pos = list(board["board"].keys())
fields_next_to_pos = []

for pos in all_pos:
    vicinity = []
    let = pos[0]
    nr = pos[1]
    for other_pos in all_pos:
        olet = other_pos[0]
        onr = other_pos[1]
        diflet = letters.index(let) - letters.index(olet)
        diflet = abs(diflet)
        difnr = numbers.index(nr) - numbers.index(onr)
        difnr = abs(difnr)
        if (diflet == 0 and difnr == 1) or (diflet == 1 and difnr == 0):
            vicinity.append(other_pos)
    fields_next_to_pos.append(vicinity)

for nr in range(len(all_pos)):
    board["next_fields"][all_pos[nr]] = fields_next_to_pos[nr]



# ####################################### print board func

def print_board(boardd):
    player = boardd["turn"] % 2 + 1
    max_length = 0
    for key in boardd["board"]:
        if len(boardd["board"][key]) > max_length:
            max_length = len(boardd["board"][key])
    print("turn nr: ", boardd["turn"])
    print("white_stones", boardd["white_stones"])
    print("black_stones", boardd["black_stones"])
    print("white_capstones", boardd["white_capstones"])
    print("black_capstones", boardd["black_capstones"])
    print("Next Player: ", player)
    line_list = []
    line_list.append(f"     0")
    for line in numbers[1:]:
        line_list.append(((max_length * 5) + 6) * " " + f"{line}")
    print(line_list)
    for column in letters:
        col_list = []
        col_list.append(column)
        for line in numbers:
            col_list.append(boardd["board"][(column, line)])
            _ = (((max_length - len(boardd["board"][(column, line)])) * 5) + 3) * " "
            col_list.append(_)
        print(col_list)
        print()


# ######################################## place func

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
                    # print("no more stones left")

            elif what_stone == "wall":
                stone = -1 * player
                if player == 1 and board["white_stones"] > 0:
                    board["white_stones"] -= 1
                elif player == 2 and board["black_stones"] > 0:
                    board["black_stones"] -= 1
                else:
                    check = 1
                    # print("no more stones left")

            elif what_stone == "capstone":
                stone = str(10 * player)
                if player == 1 and board["white_capstones"] > 0:
                    board["white_capstones"] -= 1
                elif player == 2 and board["black_capstones"] > 0:
                    board["black_capstones"] -= 1
                else:
                    check = 1
                    # print("no more stones left")

            if stone != 0 and check == 0:
                board["board"][pos].append(stone)
                board["turn"] += 1
                return board


# #################################### move func


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
        else:  # theres a wall, but is there a capstone?
            if int(board["board"][pos][-1]) > 7 and drops[-1] == 1:
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


# ########################################## is won func


def is_won(board):
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

    def is_road_piece(pos):
        if len(board["board"][pos]) > 0:
            top_piece = int(board["board"][pos][-1])
            if top_piece == player:
                return True
            elif top_piece == 10 * player:
                return True
        return False

    def is_road(lischht):
        for groups in lischht:
            top = 0
            bottom = 0
            right = 0
            left = 0
            for elem in groups:
                if elem[0] == "a":
                    top = 1
                if elem[0] == letters[-1]:
                    bottom = 1
                if elem[1] == "0":
                    left = 1
                if elem[1] == numbers[-1]:
                    right = 1
            vert = top + bottom
            horiz = right + left
            if vert == 2 or horiz == 2:
                return player
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

        def get_road_pieces():
            road_pieces = []
            for pos in board["board"].keys():
                if is_road_piece(pos):
                    road_pieces.append(pos)
            return road_pieces

        def make_groups(lischte):
            all_road_pos = get_road_pieces()
            list_with_groups = []
            already_checked = set()
            while len(all_road_pos) > 0:
                new_group = []
                new_group.append(all_road_pos[0])
                all_road_pos.remove(all_road_pos[0])
                already_checked.add(all_road_pos[0])
                list_with_pos_to_check = []
                for pos in board["next_fields"][all_road_pos[0]]:
                    list_with_pos_to_check.append(pos)
                while len(list_with_pos_to_check) > 0:
                    checking_pos = list_with_pos_to_check[0]
                    already_checked.add(checking_pos)
                    list_with_pos_to_check.remove(checking_pos)
                    if is_road_piece(checking_pos):
                        for pos in board["next_fields"][checking_pos]:
                            if pos not in already_checked:
                                list_with_pos_to_check.append(pos)
                        new_group.append(checking_pos)
                list_with_groups.append(new_group)
