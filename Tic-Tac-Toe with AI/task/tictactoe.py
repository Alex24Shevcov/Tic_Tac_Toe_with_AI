import random
import re

matrix_crossbones = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]


def show_cell() -> None:
    print("---------")
    for arr in matrix_crossbones:
        print("|", *arr, "|")
    print("---------")


def check_input_coordinates(user_input) -> bool:
    try:
        first_num, second_num = user_input.split()
        first_num = int(first_num)
        second_num = int(second_num)
    except ValueError:
        print("You should enter numbers!")
        return False

    if not (0 < first_num < 4 and 0 < second_num < 4):
        print("Coordinates should be from 1 to 3!")
        return False
    first_num -= 1
    second_num -= 1
    if matrix_crossbones[first_num][second_num] != " ":
        print("This cell is occupied! Choose another one!")
        return False

    return True


def step_bot(our_sign: str, enemy_sign: str, complexity: str) -> str:
    while True:
        unswer_who_win = who_win(complexity)
        if len(unswer_who_win) == 1:
            print(who_win(complexity)[0], end="")
            exit(0)
        elif len(unswer_who_win) == 2:
            x_or_o, indexes_or_text = who_win(complexity)
            if isinstance(indexes_or_text, str):
                print(f"{x_or_o} {indexes_or_text}", end="")
                exit(0)
            else:
                index_i = indexes_or_text[0]
                index_j = indexes_or_text[1]
                if x_or_o == "X":
                    matrix_crossbones[index_i][index_j] = "X"
                elif x_or_o == "O":
                    matrix_crossbones[index_i][index_j] = "O"
                return 'Making move level "medium"'

        if complexity == "hard":
            ...
        else:
            index_i = random.randint(0, 2)
            index_j = random.randint(0, 2)
            if matrix_crossbones[index_i][index_j] == " ":
                if our_sign == "X":
                    matrix_crossbones[index_i][index_j] = "X"
                elif our_sign == "O":
                    matrix_crossbones[index_i][index_j] = "O"
                return 'Making move level "easy"'


def step_user(for_whom, complexity):
    while True:
        if len(who_win(complexity)) != 0:
            if len(who_win(complexity)) == 1:
                print(who_win(complexity)[0], end="")
                exit(0)
            else:
                x_or_o, indexes_or_text = who_win(complexity)
                if isinstance(indexes_or_text, str):
                    print(f"{x_or_o} {indexes_or_text}", end="")
                    exit(0)

        indexes = input_coordinates()
        num_first, num_second = indexes.split()
        num_first = int(num_first) - 1
        num_second = int(num_second) - 1

        if for_whom == "X":
            matrix_crossbones[num_first][num_second] = "X"
        elif for_whom == "O":
            matrix_crossbones[num_first][num_second] = "O"
        return


def get_empty_cells():
    """Return coordinates of empty board's cells"""
    result = []
    for i in range(len(matrix_crossbones)):
        for j in range(len(matrix_crossbones)):
            if matrix_crossbones[i][j] == ' ':
                result.append((i, j))
    return result


def computer_hard_move():
    """Medium AI level and Wrapper for minimax function"""
    def minimax(new_board, player):
        """The main minimax function"""
        avail_cells = get_empty_cells()  # available cells
        # checks for the terminal states such as win, lose, and tie and returning a value accordingly
        if is_win(new_board, hu_player):
            return {'score': -10, 'index': (0, 0)}
        elif is_win(new_board, ai_player):
            return {'score': 10, 'index': (0, 0)}
        elif len(avail_cells) == 0:
            return {'score': 0, 'index': (0, 0)}
        # an array to collect all the objects
        moves = []
        # loop through available cells
        for i in range(len(avail_cells)):
            # Create an object for each and store the index of that cell
            # that was stored as a number in the object's index key
            move = {'score': 0, 'index': avail_cells[i]}

            # set the empty cell to the current player
            new_board[avail_cells[i][0]][avail_cells[i][1]] = player

            if player == ai_player:
                result = minimax(new_board, hu_player)
                move['score'] = result['score']
            else:
                result = minimax(new_board, ai_player)
                move['score'] = result['score']
            # reset the cell to empty
            new_board[avail_cells[i][0]][avail_cells[i][1]] = ' '
            moves.append(move)

        if player == ai_player:  # choose the move with the highest score
            best_move = moves.index(max(moves, key=lambda m: m['score']))
        else:  # choose the move with the lowest score
            best_move = moves.index(min(moves, key=lambda m: m['score']))
        return moves[best_move]

    ai_player = get_turn()
    hu_player = get_turn(True)
    set_move(minimax(matrix_crossbones, ai_player)['index'])


def is_win(board, player) -> bool:
    """Winning combinations using the board indexes"""
    if (board[0][0] == player and board[0][1] == player and board[0][2] == player) or \
            (board[1][0] == player and board[1][1] == player and board[1][2] == player) or \
            (board[2][0] == player and board[2][1] == player and board[2][2] == player) or \
            (board[0][0] == player and board[1][0] == player and board[2][0] == player) or \
            (board[0][1] == player and board[1][1] == player and board[2][1] == player) or \
            (board[0][2] == player and board[1][2] == player and board[2][2] == player) or \
            (board[0][0] == player and board[1][1] == player and board[2][2] == player) or \
            (board[2][0] == player and board[1][1] == player and board[0][2] == player):
        return True
    else:
        return False


def set_move(coordinates):
    turn = get_turn()
    matrix_crossbones[coordinates[0]][coordinates[1]] = turn


def get_turn(reverse: bool = False) -> 'O or X':
    x_count, o_count = 0, 0
    for line in matrix_crossbones:
        x_count += line.count('X')
        o_count += line.count('O')
    if reverse:
        return 'X' if o_count < x_count else 'O'
    return 'X' if o_count >= x_count else 'O'


def who_win(complexity) -> tuple:
    space_indexes = None
    # по вертикали
    for i in range(3):
        count_x = 0
        count_o = 0
        count_spaces = 0
        for j in range(3):
            if matrix_crossbones[j][i] == "X":
                count_x += 1
            elif matrix_crossbones[j][i] == "O":
                count_o += 1
            elif matrix_crossbones[j][i] == " ":
                space_indexes = j, i
                count_spaces += 1

        if count_x == 3:
            return "X", "wins"
        elif count_o == 3:
            return "O", "wins"

        if complexity == "medium":
            if count_spaces == 1 and count_x == 2:
                return "X", space_indexes
            elif count_spaces == 1 and count_o == 2:
                return "O", space_indexes

    # по горизонтали
    for i in range(3):
        count_x = 0
        count_o = 0
        count_spaces = 0
        for j in range(3):
            if matrix_crossbones[i][j] == "X":
                count_x += 1
            elif matrix_crossbones[i][j] == "O":
                count_o += 1
            elif matrix_crossbones[i][j] == " ":
                space_indexes = i, j
                count_spaces += 1

        if count_x == 3:
            return "X", "wins"
        elif count_o == 3:
            return "O", "wins"

        if complexity == "medium":
            if count_spaces == 1 and count_x == 2:
                return "X", space_indexes
            elif count_spaces == 1 and count_o == 2:
                return "O", space_indexes

    # главная диагональ
    count_x = 0
    count_o = 0
    count_spaces = 0
    for i in range(3):
        for j in range(3):
            if i == j:
                if matrix_crossbones[i][j] == "X":
                    count_x += 1
                elif matrix_crossbones[i][j] == "O":
                    count_o += 1
                elif matrix_crossbones[i][j] == " ":
                    space_indexes = i, j
                    count_spaces += 1

    if count_x == 3:
        return "X", "wins"
    elif count_o == 3:
        return "O", "wins"

    if complexity == "medium":
        if count_spaces == 1 and count_x == 2:
            return "X", space_indexes
        elif count_spaces == 1 and count_o == 2:
            return "O", space_indexes

    # побочная диагональ
    count_x = 0
    count_o = 0
    count_spaces = 0
    for i in range(3):
        if matrix_crossbones[i][len(matrix_crossbones[i]) - (i + 1)] == "X":
            count_x += 1
        elif matrix_crossbones[i][len(matrix_crossbones[i]) - (i + 1)] == "O":
            count_o += 1
        elif matrix_crossbones[i][len(matrix_crossbones[i]) - (i + 1)] == " ":
            space_indexes = i, len(matrix_crossbones[i]) - (i + 1)
            count_spaces += 1

    if count_x == 3:
        return "X", "wins"
    elif count_o == 3:
        return "O", "wins"

    if complexity == "medium":
        if count_spaces == 1 and count_x == 2:
            return "X", space_indexes
        elif count_spaces == 1 and count_o == 2:
            return "O", space_indexes

    have_spaces = False
    for i in range(3):
        if matrix_crossbones[i].count(" ") > 0:
            have_spaces = True
            break

    if not have_spaces:
        return "Draw",
    else:
        return ()


def input_coordinates() -> str:
    while True:
        indexes = input("Enter the coordinates: ")
        if check_input_coordinates(indexes):
            return indexes


def input_command() -> tuple:
    while True:
        try:
            input_user = input("Input command: ")
            if not (re.search(r"^start\s+(easy|user|medium|hard)\s+(easy|user|medium|hard)$", input_user) or re.search("^exit$", input_user)):
                raise ValueError
            else:
                break
        except ValueError:
            print("Bad parameters!")

    if input_user == "exit":
        exit(0)

    first_com, sec_com, third_com = input_user.split()

    return sec_com, third_com


if __name__ == "__main__":
    user_command = input_command()
    if user_command[0] == "hard" and user_command[1] == "hard":
        while True:
            show_cell()
            print('Making move level "hard"')
            computer_hard_move()
            if len(who_win("hard")) == 1:
                print(who_win("hard")[0], end="")
                exit(0)

    elif user_command[0] == "user" and user_command[1] == "hard":
        while True:
            show_cell()
            step_user("X", "")
            show_cell()
            print('Making move level "hard"')
            computer_hard_move()

    elif user_command[0] == "hard" and user_command[1] == "user":
        while True:
            show_cell()
            print('Making move level "hard"')
            computer_hard_move()
            show_cell()
            step_user("O", "")

    elif user_command[0] == "user" and user_command[1] != "user":
        while True:
            show_cell()
            step_user("X", "medium")
            show_cell()
            print(step_bot("O", "X", user_command[1]))

    elif user_command[0] != "user" and user_command[1] == "user":
        while True:
            show_cell()
            print(step_bot("O", "X", user_command[0]))
            show_cell()
            step_user("O", "medium")

    elif user_command[0] == "user" and user_command[1] == "user":
        while True:
            show_cell()
            step_user("X", "")
            show_cell()
            step_user("O", "")
    else:
        while True:
            show_cell()
            print(step_bot("X", "O", user_command[0]))
            show_cell()
            print(step_bot("O", "X", user_command[1]))


