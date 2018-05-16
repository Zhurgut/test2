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

# end of config


if board_size == 3:
    nr_of_stones = 10
    nr_of_capstones = 0
elif board_size == 4:
    nr_of_stones = 15
    nr_of_capstones = 1
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
        board["board"][(letter, str(nr))] = ["2", "1", -1]


def print_board():
    global board
    player = board["turn"] % 2 + 1
    max_length = 0
    for key in board["board"]:
        if len(board["board"][key]) > max_length:
            max_length = len(board["board"][key])
    max_length += 1
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


def move(pos, direction, drops):
    global turns, board, board_size, letters, numbers, directions
    nr_of_stones_taken = sum(drops)
    player = board["turn"] % 2 + 1

    # conditions
    a = pos in board["board"].keys()
    aa = board["board"][pos] != []
    b = direction in directions
    c = nr_of_stones_taken <= board_size
    cc = len(board["board"][pos]) >= nr_of_stones_taken
    ccc = len(drops) < board_size
    d = abs(int(board["board"][pos][-1])) % 9 == player
    if direction == "up":
        bb = pos[0] in letters[len(drops):]
    elif direction == "down":
        bb = pos[0] in letters[:(board_size - len(drops))]
    elif direction == "right":
        bb = pos[1] in numbers[:(board_size - len(drops))]
    elif direction == "left":
        bb = pos[1] in numbers[len(drops):]

    print(a, aa, b, bb, c, cc, ccc, d)

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
            if direction == "up":
                dube = letters.index(pos[0])
                for wall in relevant_walls:
                    if wall[1] == pos[1] \
                            and wall[0] in letters[dube - len(drops):dube]:
                        rly_relevant_walls.append(wall)
            elif direction == "down":
                dube = letters.index(pos[0]) + 1
                for wall in relevant_walls:
                    if wall[1] == pos[1] \
                            and wall[0] in letters[dube:dube + len(drops)]:
                        rly_relevant_walls.append(wall)
            elif direction == "right":
                dube = numbers.index(pos[1]) + 1
                for wall in relevant_walls:
                    if wall[0] == pos[0] \
                            and wall[1] in numbers[dube:dube + len(drops)]:
                        rly_relevant_walls.append(wall)
            elif direction == "left":
                dube = numbers.index(pos[1])
                for wall in relevant_walls:
                    if wall[0] == pos[0] \
                            and wall[1] in numbers[dube - len(drops):dube]:
                        rly_relevant_walls.append(wall)

        if len(rly_relevant_walls) > 1:
            return False
        elif len(rly_relevant_walls) == 0:
            return True
        else:
            # now we've got one fucken wall in our way. here we determine, whether there is a capstone to crush it or not.
            if int(board["board"][pos][-1]) > 7 and drops[-1] == 1:  # its a capstone and there is a last drop of only the capstone
                pass !!!!!!!!!!!!!!!!!!!
            else:
                return False

        print(rly_relevant_walls)

    print(check_for_walls())


place(("a", "0"), "wall")
place(("b", "1"), "wall")
place(("a", "2"), "wall")
place(("a", "1"), "capstone")

print_board()

move(("a", "2"), "down", [1, 1, 1])
