import itertools as it
import copy
import random
import time

# config:

board_size = 4

# weights for value of board function:
# with these you can determine what the computer should focus more strongly on
super = 1.7       # nr of stones that count for a road
potent = 5     # nr of stones hidden in stacks of ones own controle
cappot = 8    # nr of stones hidden in a stack under the capstone
threat = 8     # nr of moves it takes to win

# ################################################### stuff

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

    # if board["turn"] < board_size * 2 - 1:
    #     return None

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


    def cleaner(lischt):
        new_lischt = []
        for group in lischt:
            if len(group) >= board_size:
                new_lischt.append(group)
        return new_lischt


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

    def make_groups():
        all_road_pos = get_road_pieces()
        list_with_groups = []
        already_checked = set()
        while len(all_road_pos) > 0:
            new_group = []
            # print("first while loop")
            checking = all_road_pos[0]
            if checking not in already_checked:
                # print("making new group")
                new_group.append(checking)
                already_checked.add(checking)
                list_with_pos_to_check = []
                for pos in board["next_fields"][checking]:
                    list_with_pos_to_check.append(pos)
                while len(list_with_pos_to_check) > 0:
                    # print("second while loop")
                    # print("ac ", already_checked)
                    # print("pos to c ", list_with_pos_to_check)
                    checking_pos = list_with_pos_to_check[0]
                    already_checked.add(checking_pos)
                    list_with_pos_to_check.remove(checking_pos)
                    if is_road_piece(checking_pos):
                        for pos in board["next_fields"][checking_pos]:
                            if pos not in already_checked:
                                list_with_pos_to_check.append(pos)
                        new_group.append(checking_pos)
            if len(new_group) > 0:
                list_with_groups.append(new_group)
            all_road_pos.remove(checking)
        # print(list_with_groups)
        return list_with_groups

    check_first_player = is_road(cleaner(make_groups()))
    if check_first_player is not None:
        return check_first_player

    player = 3 - player

    check_second_player = is_road(cleaner(make_groups()))
    if check_second_player is not None:
        return check_second_player

    if stones_leftw == 0 or stones_leftb == 0:
        return whohasmoretopstones()

    condizio = True
    for keys in board["board"].keys():
        if board["board"][keys] == []:
            condizio = False
            break
    if condizio:
        return whohasmoretopstones()


# ################################# get all moves fuck


def get_all_moves(bret):
    bret1 = copy.deepcopy(bret)
    bret_before_move = copy.deepcopy(bret1)
    scrambled_keys_old = list(bret1["board"].keys())
    random.shuffle(scrambled_keys_old)
    b_and_cs = []
    emptis = []
    rest = []
    for feld in scrambled_keys_old:
        if bret1["board"][feld] == [] and (feld[0] == "b" or feld[0] == "1"):
            b_and_cs.append(feld)
        elif bret1["board"][feld] == []:
            emptis.append(feld)
        else:
            rest.append(feld)
    scrambled_keys = b_and_cs + emptis + rest
    for position in scrambled_keys:
        if bret1["board"][position] == []:
            for type in types:
                place(bret1, position, type)
                if bret1["turn"] > bret_before_move["turn"]:
                    bret_after_move = copy.deepcopy(bret1)
                    bret1 = copy.deepcopy(bret_before_move)
                    yield bret_after_move
        else:
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
            for direction in directions:
                for drop_pattern in drop_list:
                    bret_before_move = copy.deepcopy(bret1)
                    move(bret1, position, direction, drop_pattern)
                    if bret1["turn"] > bret_before_move["turn"]:
                        bret_after_move = copy.deepcopy(bret1)
                        bret1 = copy.deepcopy(bret_before_move)


                        yield bret_after_move


# ################################# get all try to win moves

def get_all_try_to_win_moves(bret):

    bret1 = copy.deepcopy(bret)
    bret_before_move = copy.deepcopy(bret1)
    scrambled_keys = set(bret1["board"].keys())
    player = bret1["turn"] % 2 + 1

    for position in scrambled_keys:
        if bret1["board"][position] == []:
            play_pos = False
            for next_pos in bret1["next_fields"][position]:
                stack_at_next = bret1["board"][next_pos]
                if stack_at_next != []:
                    if int(stack_at_next[-1]) % 9 == player:
                        play_pos = True
                        break
            if play_pos:
                place(bret1, position, "normal")
                bret_after_move = copy.deepcopy(bret1)
                bret1 = copy.deepcopy(bret_before_move)
                yield bret_after_move
        else:
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
            for direction in directions:
                for drop_pattern in drop_list:
                    bret_before_move = copy.deepcopy(bret1)
                    move(bret1, position, direction, drop_pattern)
                    if bret1["turn"] > bret_before_move["turn"]:
                        bret_after_move = copy.deepcopy(bret1)
                        bret1 = copy.deepcopy(bret_before_move)
                        yield bret_after_move

# ############################### get no winning moves


def get_no_winning_moves(bret):

    if is_won(bret) is not None:
        return bret

    player = (bret["turn"] % 2) + 1
    opponent = 3 - player
    for move in get_all_moves(bret):
        has_winning_for_op = False
        for new_move in get_all_try_to_win_moves(move):
            if is_won(new_move) == opponent:
                has_winning_for_op = True
                break
        if not has_winning_for_op:
            yield move

# ################################## get value


def get_value(bret):
    road_stones_w = 0       # weights: super
    road_stones_b = 0
    stones_in_stack_w = 0     # potent
    stones_in_stack_b = 0
    stones_under_cap_w = 0      # cappot
    stones_under_cap_b = 0
    moves_to_win_w = 3          # threat
    moves_to_win_b = 3

    for pos in bret["board"].values():
        if len(pos) > 0:
            if len(pos) == 1:  # single stones
                if pos[0] == "1" or pos[0] == "10":
                    road_stones_w += 1
                elif pos[0] == "2" or pos[0] == "20":
                    road_stones_b += 1

            else:  # stacks
                if len(pos) > board_size + 1:
                    pos = pos[-1 * (board_size + 1):-1]
                if abs(int(pos[-1])) % 9 == 1:  # if the stack belongs to white
                    if pos[-1] == "1" or pos[-1] == "10":
                        road_stones_w += 1
                    if pos[-1] == "10":
                        for stone in pos[:-1]:
                            if stone == "1":
                                stones_under_cap_w += 1
                    else:
                        for stone in pos[:-1]:
                            if stone == "1":
                                stones_in_stack_w += 1
                else:  # the stack belongs to black
                    if pos[-1] == "2" or pos[-1] == "20":
                        road_stones_b += 1
                    if pos[-1] == "20":
                        for stone in pos[:-1]:
                            if stone == "2":
                                stones_under_cap_b += 1
                    else:
                        for stone in pos[:-1]:
                            if stone == "2":
                                stones_in_stack_b += 1

    def get_nr_of_moves_to_win(bret):
        player = bret["turn"] % 2 + 1
        nr_to_win = 3
        if is_won(bret) == player:
            nr_to_win = 0
        if nr_to_win == 3:
            for new_bret in get_all_try_to_win_moves(bret):
                if is_won(new_bret) == player:
                    nr_to_win = 1
                    break
        if nr_to_win == 3:
            for new_bret in get_all_try_to_win_moves(bret):
                new_bret["turn"] -= 1
                for new_new_bret in get_all_try_to_win_moves(new_bret):
                    if is_won(new_new_bret) == player:
                        nr_to_win = 2
                        break
                if nr_to_win == 2:
                    break
        return nr_to_win

    player = bret["turn"] % 2 + 1
    if player == 1:
        moves_to_win_w = get_nr_of_moves_to_win(bret)
        bret["turn"] -= 1
        moves_to_win_b = get_nr_of_moves_to_win(bret)
        bret["turn"] += 1
    else:
        moves_to_win_b = get_nr_of_moves_to_win(bret)
        bret["turn"] -= 1
        moves_to_win_w = get_nr_of_moves_to_win(bret)
        bret["turn"] += 1

    black1 = road_stones_b ** super + 1
    black2 = stones_in_stack_b * potent + 1
    black3 = stones_under_cap_b * cappot + 1
    black4 = threat ** (3 - moves_to_win_b)
    black = black1 * black2 * black3 * black4 + 0.0000000001
    white1 = road_stones_w ** super + 1
    white2 = stones_in_stack_w * potent + 1
    white3 = stones_under_cap_w * cappot + 1
    white4 = threat ** (3 - moves_to_win_w)
    white = white1 * white2 * white3 * white4 + 0.0000000001

    value = black / white

    # print("moves to win white ", moves_to_win_w)
    # print("moves to win black ", moves_to_win_b)
    # print("value ", value)
    return value




# ################################## get human move


def get_human_move():
    global board
    bret_before = copy.deepcopy(board)
    move_made = False
    print_board(board)
    while not move_made:
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
            if board["turn"] > bret_before["turn"]:
                move_made = True
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
            if board["turn"] > bret_before["turn"]:
                move_made = True


# ############################################## get good moves stuff:


def get_aprox_val_limit(breet, confine):
    low_val = 100
    high_val = 0
    for move in get_no_winning_moves(breet):
        val = get_value(move)
        if val < low_val:
            low_val = copy.copy(val)
        if val > high_val:
            high_val = copy.copy(val)
    player = breet["turn"] % 2 + 1
    if player == 2:
        limit = high_val - ((high_val - low_val + 0.001) / confine)
    else:
        limit = low_val + ((high_val - low_val + 0.001) / confine)
    return limit


def get_good_moves(breet, stop_at, confine):
    stopper = 0
    limit = get_aprox_val_limit(breet, confine)
    player = breet["turn"] % 2 + 1
    if player == 2:
        for move in get_no_winning_moves(breet):
            if get_value(move) > limit and stopper < stop_at:
                yield move
                stopper += 1
    else:
        for move in get_no_winning_moves(breet):
            if get_value(move) < limit and stopper < stop_at:
                yield move
                stopper += 1

# ################################# get BEST move


def get_best_move_black(bred):
    if is_won(bred) is not None:
        return bred
    nr_of_no_winning_moves = 0
    for move in get_all_moves(bred):
        if is_won(move) == 2:
            return move
    for move in get_no_winning_moves(bred):
        nr_of_no_winning_moves += 1
    if nr_of_no_winning_moves == 1:
        return next(get_no_winning_moves(bred))

    nrs = 0
    average = 0
    buffer_bred = copy.deepcopy(bred)
    for move_bred in get_good_moves(bred, 5, 4):
        val1 = get_value(move_bred)
        for after_move_bred in get_good_moves(move_bred, 3, 100):
            val2 = get_value(after_move_bred)
            for after_after in get_good_moves(after_move_bred, 3, 7):
                val3 = get_value(after_after)
                for after_that in get_good_moves(after_after, 1, 100):
                    val4 = get_value(after_that)
                    nrs += 1

                    new_avg = val1 * val2 * val3 * val4
                    if new_avg > average:
                        print("new avg: ", new_avg)
                        average = copy.copy(new_avg)
                        buffer_bred = copy.deepcopy(move_bred)
    print(f"checked {nrs} variations for blacks next move")
    return buffer_bred



# ########################################### here we go...


while True:
    aa = 0
    ab = 0
    ac = 0
    ad = 0
    get_human_move()
    print(get_value(board))
    for movess in get_all_moves(board):
        aa += 1
    for movesss in get_no_winning_moves(board):
        ab += 1
    for movessss in get_all_try_to_win_moves(board):
        ac += 1
    for movesssss in get_good_moves(board, 5, 4):
        ad += 1
    print("for blacks next move")
    print(f"there are {aa} possible moves, {ab} of them are not winning and\
 {ac} are returned by the try_to_win moves function")
    print(f"there are {ad} good moves returned")
    print()

    aa = 0
    ab = 0
    ac = 0
    ad = 0
    board = get_best_move_black(board)
    print("value after black played ", get_value(board))
    for movess in get_all_moves(board):
        aa += 1
    for movesss in get_no_winning_moves(board):
        ab += 1
    for movessss in get_all_try_to_win_moves(board):
        ac += 1
    for movesssss in get_good_moves(board, 5, 4):
        ad += 1
    print("for white")
    print(f"there are {aa} possible moves, {ab} of them are not winning and\
 {ac} are returned by the try_to_win moves function")
    print(f"there are {ad} good moves returned")
    print()




# for nr in range(15):
#     get_human_move()
#     print(is_won(board))
#
# time1 = time.time()
# a = 0
# for bret in get_all_moves(board):
#     for new in get_all_try_to_win_moves(bret):
#         print(is_won(new))
#         a += 1
#
# time2 = time.time()
#
# print(f"generated {a} boards in {time2-time1} seconds")
# print(time1)
# print(time2)
# print((time2-time1)/a)
