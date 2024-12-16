import tkinter as tk
import random

# Глобальные переменные
result_frame = game_frame = active_player = grid = btns = user_symbol = ai_symbol = None

def is_winner(grid, player):  # Проверка победителя
    for idx in range(3):
        if all(grid[idx][j] == player for j in range(3)) or all(grid[j][idx] == player for j in range(3)):
            return True
    if grid[0][0] == grid[1][1] == grid[2][2] == player or grid[0][2] == grid[1][1] == grid[2][0] == player:
        return True
    return False

def is_draw(grid):
    return all(grid[i][j] != "" for i in range(3) for j in range(3))

def end_game(message):
    global result_frame
    result_frame = tk.Toplevel()
    result_frame.title("Игра окончена")
    tk.Label(result_frame, text=message, font=("Helvetica", 24)).pack(padx=20, pady=20)
    tk.Button(result_frame, text="Новая игра", command=reset_game).pack(pady=10)
    tk.Button(result_frame, text="Выход", command=result_frame.quit).pack(pady=10)

def reset_game():
    game_frame.destroy()
    result_frame.destroy()
    main_menu.deiconify()

def initiate_game_X():  # Начало игры для крестиков
    global active_player, grid, btns, user_symbol, ai_symbol, game_frame
    grid = [["" for _ in range(3)] for _ in range(3)]
    user_symbol, ai_symbol, active_player = "X", "O", "X"
    btns = [[None for _ in range(3)] for _ in range(3)]
    game_frame = tk.Toplevel(main_menu)
    game_frame.title("Крестики-нолики")
    for i in range(3):
        for j in range(3):
            btns[i][j] = tk.Button(game_frame, text="", width=10, height=3, font=("Helvetica", 24),
                                   command=lambda i=i, j=j: player_move(i, j))
            btns[i][j].grid(row=i, column=j)
    main_menu.withdraw()

def initiate_game_O():  # Начало игры для ноликов
    global active_player, grid, btns, user_symbol, ai_symbol, game_frame
    grid = [["" for _ in range(3)] for _ in range(3)]
    user_symbol = "O"
    ai_symbol = "X"
    active_player = ai_symbol
    btns = [[None for _ in range(3)] for _ in range(3)]
    game_frame = tk.Toplevel(main_menu)
    game_frame.title("Крестики-нолики")
    for i in range(3):
        for j in range(3):
            btns[i][j] = tk.Button(game_frame, text="", width=10, height=3, font=("Helvetica", 24),
                                   command=lambda i=i, j=j: player_move(i, j))
            btns[i][j].grid(row=i, column=j)
    main_menu.withdraw()
    ai_first_move()

def player_move(i, j):
    global active_player
    if grid[i][j] == "":
        grid[i][j] = active_player
        btns[i][j].config(text=active_player, state="disabled")
        if is_winner(grid, active_player):
            end_game(f"Игрок ({active_player}) выиграл!")
            return
        if is_draw(grid):
            end_game("Ничья!")
            return
        active_player = ai_symbol if active_player == user_symbol else user_symbol
        if active_player == ai_symbol:
            ai_move()

def ai_move():  # Ход компьютера
    global active_player
    best_move = None
    best_value = float('-inf')


    for i in range(3):
        for j in range(3):
            if grid[i][j] == "":
                grid[i][j] = ai_symbol
                if is_winner(grid, ai_symbol):
                    best_move = (i, j)
                    grid[i][j] = ""
                    break
                grid[i][j] = ""
    if best_move is None:
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    grid[i][j] = user_symbol
                    if is_winner(grid, user_symbol):
                        best_move = (i, j)
                        grid[i][j] = ""
                        break
                    grid[i][j] = ""
    if best_move is None:
        best_value = float('-inf')
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    grid[i][j] = ai_symbol
                    move_value = minimax(grid, 0, False, float('-inf'), float('inf'))
                    grid[i][j] = ""
                    if move_value > best_value:
                        best_value = move_value
                        best_move = (i, j)

    if best_move:
        row, col = best_move
        grid[row][col] = ai_symbol
        btns[row][col].config(text=ai_symbol, state="disabled")
    if is_winner(grid, ai_symbol):
        end_game(f"Компьютер ({ai_symbol}) выиграл!")
        return
    if is_draw(grid):
        end_game("Ничья!")
        return

    active_player = user_symbol

def ai_first_move():  # Первый ход компьютера
    global active_player
    available_moves = [(i, j) for i in range(3) for j in range(3) if grid[i][j] == ""]
    first_move = random.choice(available_moves)
    row, col = first_move
    grid[row][col] = ai_symbol
    btns[row][col].config(text=ai_symbol, state="disabled")
    active_player = user_symbol

def minimax(grid, depth, is_maximizing, alpha, beta):
    if is_winner(grid, ai_symbol): return 1
    if is_winner(grid, user_symbol): return -1
    if is_draw(grid): return 0
    if is_maximizing:
        max_eval = float('-inf')
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    grid[i][j] = ai_symbol
                    eval = minimax(grid, depth + 1, False, alpha, beta)
                    grid[i][j] = ""
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha: break
        return max_eval
    else:
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if grid[i][j] == "":
                    grid[i][j] = user_symbol
                    eval = minimax(grid, depth + 1, True, alpha, beta)
                    grid[i][j] = ""
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha: break
        return min_eval

# Начальное окно выбора
main_menu = tk.Tk()
main_menu.title("Выбор игры")
tk.Button(main_menu, text="Играть за крестики", width=20, height=2, font=("Helvetica", 14), command=initiate_game_X).pack(pady=5)
tk.Button(main_menu, text="Играть за нолики", width=20, height=2, font=("Helvetica", 14), command=initiate_game_O).pack(pady=5)
main_menu.mainloop()
