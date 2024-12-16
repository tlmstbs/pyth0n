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
    center_window(result_window, 400, 250)

    tk.Label(result_window, text=message, font=("Arial", 18, "bold"), fg="white", bg="darkblue", pady=20).pack(fill="both")
    tk.Button(result_window, text="Новый раунд", font=("Arial", 14), bg="lightgreen", command=start_new_game).pack(pady=10, padx=20, fill="x")
    tk.Button(result_window, text="Закрыть", font=("Arial", 14), bg="red", fg="white", command=result_window.quit).pack(pady=10, padx=20, fill="x")

def start_new_game():
    game_window.destroy()
    result_window.destroy()
    start_game_window.deiconify()

def create_game_window():
    global game_window
    game_window = tk.Toplevel(start_game_window)
    game_window.title("Крестики-нолики")
    center_window(game_window, 600, 500)
    game_window.configure(bg="lightgray")

def start_game_X():
    global current_player, board, buttons, player_symbol, computer_symbol
    board = [["" for _ in range(3)] for _ in range(3)]
    player_symbol, computer_symbol, current_player = "X", "O", "X"
    buttons = [[None for _ in range(3)] for _ in range(3)]
    create_game_window()
    draw_board()
    start_game_window.withdraw()

def start_game_O():
    global current_player, board, buttons, player_symbol, computer_symbol
    board = [["" for _ in range(3)] for _ in range(3)]
    player_symbol, computer_symbol = "O", "X"
    current_player = computer_symbol
    buttons = [[None for _ in range(3)] for _ in range(3)]
    create_game_window()
    draw_board()
    computer_turn_first()
    start_game_window.withdraw()

def draw_board():
    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(
                game_window, text="", width=10, height=4, font=("Arial", 18, "bold"),
                bg="white", activebackground="lightblue",
                command=lambda i=i, j=j: player_turn(i, j)
            )
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

def player_turn(i, j):
    global current_player
    if board[i][j] == "":
        board[i][j] = current_player
        buttons[i][j].config(text=current_player, state="disabled", disabledforeground="black")
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

    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = computer_symbol
                if check_winner(board, computer_symbol):
                    best_move = (i, j)
                    board[i][j] = ""
                    break
                board[i][j] = ""
    if best_move is None:
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = player_symbol
                    if check_winner(board, player_symbol):
                        best_move = (i, j)
                        board[i][j] = ""
                        break
                    board[i][j] = ""
    if best_move is None:
        available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
        best_move = random.choice(available_moves)

    row, col = best_move
    board[row][col] = computer_symbol
    buttons[row][col].config(text=computer_symbol, state="disabled", disabledforeground="black")

    if check_winner(board, computer_symbol):
        game_over(f"Компьютер ({computer_symbol}) победил!")
        return
    if check_draw(board):
        game_over("Ничья!")
        return

    current_player = player_symbol

def computer_turn_first():
    global current_player
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
    first_move = random.choice(available_moves)
    row, col = first_move
    board[row][col] = computer_symbol
    buttons[row][col].config(text=computer_symbol, state="disabled", disabledforeground="black")
    current_player = player_symbol

# Начальное окно выбора
start_game_window = tk.Tk()
start_game_window.title("Крестики-нолики")
center_window(start_game_window, 400, 300)
start_game_window.configure(bg="lightblue")

header = tk.Label(start_game_window, text="Выберите сторону", font=("Arial", 20, "bold"), bg="lightblue", fg="darkblue")
header.pack(pady=20)

tk.Button(start_game_window, text="Играть за X", font=("Arial", 14), bg="white", command=start_game_X).pack(pady=10, fill="x", padx=50)
tk.Button(start_game_window, text="Играть за O", font=("Arial", 14), bg="white", command=start_game_O).pack(pady=10, fill="x", padx=50)

start_game_window.mainloop()
