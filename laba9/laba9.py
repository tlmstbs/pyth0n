import tkinter as tk
import random

# Глобальные переменные
result_window = game_window = current_player = board = buttons = player_symbol = computer_symbol = None

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')

def check_winner(board, player):
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False

def check_draw(board):
    return all(board[i][j] != "" for i in range(3) for j in range(3))

def game_over(message):
    global result_window
    result_window = tk.Toplevel()
    result_window.title("Конец игры")
    center_window(result_window, 400, 200)
    tk.Label(result_window, text=message, font=("Arial", 24)).pack(padx=20, pady=20)
    tk.Button(result_window, text="Новый раунд", command=start_new_game).pack(pady=10)
    tk.Button(result_window, text="Закрыть", command=result_window.quit).pack(pady=10)

def start_new_game():
    game_window.destroy()
    result_window.destroy()
    start_game_window.deiconify()

def start_game_X():
    global current_player, board, buttons, player_symbol, computer_symbol, game_window
    initialize_game("X", "O")

def start_game_O():
    global current_player, board, buttons, player_symbol, computer_symbol, game_window
    initialize_game("O", "X")
    computer_turn()

def initialize_game(player_sym, computer_sym):
    global current_player, board, buttons, player_symbol, computer_symbol, game_window
    player_symbol, computer_symbol, current_player = player_sym, computer_sym, "X"
    board = [["" for _ in range(3)] for _ in range(3)]
    buttons = [[None for _ in range(3)] for _ in range(3)]

    game_window = tk.Toplevel(start_game_window)
    game_window.title("Крестики-нолики: Игра")
    center_window(game_window, 600, 400)

    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(game_window, text="", width=10, height=3, font=("Arial", 24),
                                      command=lambda i=i, j=j: player_turn(i, j))
            buttons[i][j].grid(row=i, column=j)

    start_game_window.withdraw()

def player_turn(i, j):
    global current_player
    if board[i][j] == "":
        board[i][j] = current_player
        buttons[i][j].config(text=current_player, state="disabled")

        if check_winner(board, current_player):
            game_over(f"Игрок ({current_player}) победил!")
            return
        if check_draw(board):
            game_over("Ничья!")
            return

        current_player = computer_symbol if current_player == player_symbol else player_symbol

        if current_player == computer_symbol:
            computer_turn()

def computer_turn():
    global current_player
    best_move = None
    best_value = float('-inf')

    # Минимакс для поиска лучшего хода
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = computer_symbol
                move_value = minimax(board, 0, False, float('-inf'), float('inf'))
                board[i][j] = ""
                if move_value > best_value:
                    best_value = move_value
                    best_move = (i, j)

    if best_move:
        row, col = best_move
        board[row][col] = computer_symbol
        buttons[row][col].config(text=computer_symbol, state="disabled")

    if check_winner(board, computer_symbol):
        game_over(f"Компьютер ({computer_symbol}) победил!")
        return
    if check_draw(board):
        game_over("Ничья!")
        return

    current_player = player_symbol

def minimax(board, depth, is_maximizing, alpha, beta):
    if check_winner(board, computer_symbol):
        return 10 - depth
    if check_winner(board, player_symbol):
        return depth - 10
    if check_draw(board):
        return 0

    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = computer_symbol
                    eval = minimax(board, depth + 1, False, alpha, beta)
                    board[i][j] = ""
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = player_symbol
                    eval = minimax(board, depth + 1, True, alpha, beta)
                    board[i][j] = ""
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

# Начальное окно
start_game_window = tk.Tk()
start_game_window.title("Выбор игры")
center_window(start_game_window, 400, 200)
tk.Label(start_game_window, text="Выберите символ для игры", font=("Arial", 16)).pack(pady=10)
tk.Button(start_game_window, text="Играть за крестики", width=20, height=2, font=("Arial", 14), command=start_game_X).pack(pady=5)
tk.Button(start_game_window, text="Играть за нолики", width=20, height=2, font=("Arial", 14), command=start_game_O).pack(pady=5)
start_game_window.mainloop()
