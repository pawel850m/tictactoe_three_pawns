import time
import tkinter as tk
import boardclass as bc

NUMBER_OF_BUTTONS = 9
TIME_TO_THINK = 7.2
TIME_TO_THINK_EASY_MED = 0.1
BEST_MOVE_MAX_SCORE = 10
BEST_MOVE_MIN_SCORE = -10
NUMBER_OF_BUTTONS_TO_WIN = 3
EASY = 1
MEDIUM = 2
HARD = 3

GameBoard = bc.Board()
GameBoardCopy = bc.Board()
root = tk.Tk()
root.resizable(False, False)
root.title("3pawns tictactoe")
Main = tk.Frame(root, width=400, height=300)
Main.grid(row=1, column=0)
Top = tk.Frame(root, width=100, height=1)
Top.grid(row=0, column=0)
Board = tk.Frame(Main, width=4000, heigh=3000)
Board.pack(side=tk.LEFT)


def click(buttons, number):
    """
    Reakcja na naciśnięty przycisk.
    """
    if bc.Board.game_run:
        player(number)
        if bc.Board.update:
            bc.Board.update = 0
            bc.Board.place_delete = 0
            buttons["text"] = bc.Board.player_shape
            if win() == -1:
                win_signal(bc.Board.player_shape)
            elif win() == 1:
                win_signal(bc.Board.computer_shape)
            else:
                computer()
        if win() == -1:
            win_signal(bc.Board.player_shape)
        elif win() == 1:
            win_signal(bc.Board.computer_shape)


def win():
    """
        Sprawdzenie wygranej.
    """
    for i in range(NUMBER_OF_BUTTONS):
        GameBoardCopy.board[i] = GameBoard.board[i]
    return GameBoard.win_checker(bc.Board.player_shape, bc.Board.computer_shape)


def shape_tab_edit(button_number, shape):
    """
        Zwraca indeks listy przechowującej pionki gracza lub komputera.
    """
    for _ in range(len(bc.Board.shape_tab)):
        del bc.Board.shape_tab[0]
    for k in range(NUMBER_OF_BUTTONS):
        if GameBoardCopy.board[k] == shape:
            bc.Board.shape_tab.append(k)
    return bc.Board.shape_tab[button_number]


def player(number):
    """
        Odpowiada za możliwość poprawnego ruchu gracza.
    """
    if bc.Board.pawns_limit == 0:
        move = int(number)
        move = move - 1
        if move in range(0, NUMBER_OF_BUTTONS):
            if GameBoard.board[move] == bc.Board.computer_shape \
                    or GameBoard.board[move] == bc.Board.player_shape:
                return 0
            GameBoard.board[move] = bc.Board.player_shape
            bc.Board.update = 1
        else:
            return 0
    else:
        if bc.Board.place_delete == 0:
            move = int(number)
            move = move - 1
            if move in range(0, NUMBER_OF_BUTTONS):
                if GameBoard.board[move] == bc.Board.player_shape and bc.Board.place_delete == 0:
                    GameBoard.board[move] = ' '
                    button_number_changer(move, ' ')
                    bc.Board.place_delete = 1
            return 0

        move = number
        move = move - 1
        if move in range(0, NUMBER_OF_BUTTONS):
            if GameBoard.board[move] == bc.Board.computer_shape \
                    or GameBoard.board[move] == bc.Board.player_shape:
                return 0
            GameBoard.board[move] = bc.Board.player_shape
            bc.Board.update = 1
        return 0


def button_number_changer(number_to_change, shape):
    """
        Zmiana wyswietlanego tekstu na przycisku.
    """
    bc.Board.button_list[number_to_change]['text'] = shape


def minmax(depth=0, max_min=1):
    """
        Zwraca indeks najlepszego posunięcia dla komputera.
    """
    result = GameBoardCopy.win_checker(bc.Board.player_shape, bc.Board.computer_shape)
    if result is not None:
        return result
    if max_min:
        best_score = BEST_MOVE_MIN_SCORE
        for i in range(NUMBER_OF_BUTTONS):
            if GameBoardCopy.board[i] == " ":
                GameBoardCopy.board[i] = bc.Board.computer_shape
                score = minmax(depth + 1, 0)
                GameBoardCopy.board[i] = " "
                if best_score < score:
                    best_score = score
        return best_score
    else:
        best_score = BEST_MOVE_MAX_SCORE
        for i in range(NUMBER_OF_BUTTONS):
            if GameBoardCopy.board[i] == ' ':
                GameBoardCopy.board[i] = bc.Board.player_shape
                score = minmax(depth + 1, 1)
                GameBoardCopy.board[i] = ' '
                if best_score > score:
                    best_score = score
        return best_score


def minmax_for_three_pawns(min_max_time, depth=0, max=1, place_number=0):
    """
        Zwraca indeks najlepszego posunięcia komputera, gdy na planszy są po trzy pionki każdej ze stron.
    """
    time_start_min_max = min_max_time
    pawn_to_remove = place_number
    result = GameBoardCopy.win_checker(bc.Board.player_shape, bc.Board.computer_shape)
    if result is not None:
        return result
    if bc.Board.level == EASY:
        seconds_to_check = TIME_TO_THINK_EASY_MED
        if depth == 0:
            return 0
    if bc.Board.level == MEDIUM:
        seconds_to_check = TIME_TO_THINK_EASY_MED
        if depth == 1:
            return 0
    else:
        seconds_to_check = TIME_TO_THINK
        if depth == 4:
            return 0

    if time.time() - time_start_min_max > seconds_to_check / NUMBER_OF_BUTTONS:
        return 0

    if max:
        best_score = BEST_MOVE_MIN_SCORE
        for i in range(NUMBER_OF_BUTTONS):
            if GameBoardCopy.board[i] == " ":
                for j in range(NUMBER_OF_BUTTONS_TO_WIN):
                    index = shape_tab_edit(j, bc.Board.computer_shape)
                    GameBoardCopy.board[index] = " "
                    GameBoardCopy.board[i] = bc.Board.computer_shape

                    score = minmax_for_three_pawns(time_start_min_max, depth + 1, 0, pawn_to_remove)

                    GameBoardCopy.board[index] = bc.Board.computer_shape
                    GameBoardCopy.board[i] = " "

                    if best_score < score:
                        best_score = score

        return best_score

    else:

        best_score = BEST_MOVE_MAX_SCORE
        for i in range(NUMBER_OF_BUTTONS):
            if GameBoardCopy.board[i] == ' ':
                for j in range(NUMBER_OF_BUTTONS_TO_WIN):
                    index = shape_tab_edit(j, bc.Board.player_shape)
                    GameBoardCopy.board[index] = " "
                    GameBoardCopy.board[i] = bc.Board.player_shape

                    score = minmax_for_three_pawns(time_start_min_max, depth + 1, 1, pawn_to_remove)

                    GameBoardCopy.board[index] = bc.Board.player_shape
                    GameBoardCopy.board[i] = " "

                    if best_score > score:
                        best_score = score

        return best_score


def computer():
    """
        Odpowiada za właściwy ruch komputera.
    """
    for i in range(NUMBER_OF_BUTTONS):
        GameBoardCopy.board[i] = GameBoard.board[i]
    best_place_to_remove = 0
    best_score = BEST_MOVE_MIN_SCORE
    points = -1
    move = 0
    for i in range(NUMBER_OF_BUTTONS):
        if GameBoardCopy.board[i] == bc.Board.computer_shape:
            bc.Board.shape_tab.append(i)

    if len(bc.Board.shape_tab) > 1:
        bc.Board.pawns_limit = 1

    if len(bc.Board.shape_tab) > 2:
        for i in range(NUMBER_OF_BUTTONS):
            if GameBoardCopy.board[i] == " ":
                for computer_shape_number in range(NUMBER_OF_BUTTONS_TO_WIN):
                    remove = shape_tab_edit(computer_shape_number, bc.Board.computer_shape)
                    GameBoardCopy.board[remove] = ' '
                    GameBoardCopy.board[i] = bc.Board.computer_shape

                    min_max_time = time.time()
                    points = minmax_for_three_pawns(min_max_time, 0, 0, computer_shape_number)

                    GameBoardCopy.board[remove] = bc.Board.computer_shape
                    GameBoardCopy.board[i] = ' '

                    if best_score <= points:
                        best_score = points
                        best_place_to_remove = remove
                        move = i

                if points == 1:
                    break

        GameBoard.board[best_place_to_remove] = ' '
        button_number_changer(best_place_to_remove, ' ')
        GameBoard.board[move] = bc.Board.computer_shape
        button_number_changer(move, bc.Board.computer_shape)

    else:
        for i in range(NUMBER_OF_BUTTONS):
            if GameBoardCopy.board[i] == " ":
                GameBoardCopy.board[i] = bc.Board.computer_shape

                points = minmax(0, 0)
                GameBoardCopy.board[i] = ' '

                if best_score <= points:
                    best_score = points
                    move = i
        GameBoard.board[move] = bc.Board.computer_shape
        button_number_changer(move, bc.Board.computer_shape)

    for _ in bc.Board.shape_tab:
        del bc.Board.shape_tab[0]


def win_signal(shape):
    """
        Sprawdzenie, które pionki są wygrywające.
        Zaznaczenie wygranej.
        Reset ustawień.
    """
    win_list = (0, 0, 0)
    if GameBoard.board[0] == shape and GameBoard.board[1] == shape \
            and GameBoard.board[2] == shape:
        win_list = (0, 1, 2)

    elif GameBoard.board[3] == shape and GameBoard.board[4] == shape \
            and GameBoard.board[5] == shape:
        win_list = (3, 4, 5)

    elif GameBoard.board[6] == shape and GameBoard.board[7] == shape \
            and GameBoard.board[8] == shape:
        win_list = (6, 7, 8)

    elif GameBoard.board[0] == shape and GameBoard.board[3] == shape \
            and GameBoard.board[6] == shape:
        win_list = (0, 3, 6)

    elif GameBoard.board[1] == shape and GameBoard.board[4] == shape \
            and GameBoard.board[7] == shape:
        win_list = (1, 4, 7)

    elif GameBoard.board[2] == shape and GameBoard.board[5] == shape \
            and GameBoard.board[8] == shape:
        win_list = (2, 5, 8)

    elif GameBoard.board[0] == shape and GameBoard.board[4] == shape \
            and GameBoard.board[8] == shape:
        win_list = (0, 4, 8)

    elif GameBoard.board[2] == shape and GameBoard.board[4] == shape \
            and GameBoard.board[6] == shape:
        win_list = (2, 4, 6)
    for i in range(NUMBER_OF_BUTTONS_TO_WIN):
        bc.Board.button_list[win_list[i]].configure(fg='orange red')

    bc.Board.game_run = 0


def reset():
    """
        Reset ustawień.
    """
    bc.Board.game_run = 1
    bc.Board.pawns_limit = 0
    bc.Board.place_delete = 0

    for i in range(NUMBER_OF_BUTTONS):
        button_number_changer(i, " ")
        bc.Board.button_list[i].configure(fg='midnight blue')
        GameBoard.board[i] = " "


def set_game(shape_number, level_number):
    """
        Reset ustawień.
        Ustawienie poziomu trudności.
        Ustawienie kształtu.
    """
    reset()
    if level_number.get() == EASY:
        bc.Board.level = EASY
    elif level_number.get() == MEDIUM:
        bc.Board.level = MEDIUM
    elif level_number.get() == HARD:
        bc.Board.level = HARD
    if shape_number.get() == 1:
        bc.Board.player_shape = "X"
        bc.Board.computer_shape = "O"
    if shape_number.get() == 2:
        bc.Board.player_shape = "O"
        bc.Board.computer_shape = "X"


def show_boardgame():
    """
            Wyświetlanie okienka z grą.
    """
    row_number = 2
    column_number = 0
    for i in range(9):
        bc.Board.button_list.append(tk.Button(Board, text=" ", height=1, width=3,
                                              font='CourierNew 30 bold', bg="light grey",
                                              command=lambda i=i: click(bc.Board.button_list[i], i + 1)))
        bc.Board.button_list[i].grid(row=row_number, column=column_number)
        column_number += 1

        if i == 2:
            column_number = 0
            row_number = 3
        elif i == 5:
            column_number = 0
            row_number = 4

    level_number = tk.IntVar()
    shape_number = tk.IntVar()
    level_number.set(HARD)
    shape_number.set(1)

    menubar = tk.Menu(Top)
    file_menu = tk.Menu(menubar, tearoff=0)
    file_menu.add_command(label="Exit", command=root.quit())
    menubar.add_cascade(label="File", menu=file_menu)
    game_menu = tk.Menu(menubar, tearoff=0)
    game_menu.add_command(label="StartGame", command=lambda: set_game(shape_number, level_number))
    game_menu2 = tk.Menu(game_menu, tearoff=0)
    game_menu3 = tk.Menu(game_menu, tearoff=0)
    game_menu2.add_radiobutton(label="Easy", variable=level_number, value=EASY)
    game_menu2.add_radiobutton(label="Medium", variable=level_number, value=MEDIUM)
    game_menu2.add_radiobutton(label="Hard", variable=level_number, value=HARD)
    game_menu3.add_radiobutton(label="X", variable=shape_number, value=1)
    game_menu3.add_radiobutton(label="O", variable=shape_number, value=2)
    game_menu.add_cascade(label="Level", menu=game_menu2)
    game_menu.add_cascade(label="Shape", menu=game_menu3)
    menubar.add_cascade(label="Game", menu=game_menu)
    root.config(menu=menubar)
    root.mainloop()


def main():
    show_boardgame()


if __name__ == '__main__':
    main()
