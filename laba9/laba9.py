import tkinter as tk
import random

# Глобальные переменные
result_window = game_window = current_player = board = buttons = player_symbol = computer_symbol = None


def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()  # Ширина экрана
    screen_height = window.winfo_screenheight()  # Высота экрана
    position_top = int(screen_height / 2 - height / 2)
    position_right = int(screen_width / 2 - width / 2)
    window.geometry(f'{width}x{height}+{position_right}+{position_top}')


def check_winner(board, player):  # Проверка победителя
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)): return True
    if board[0][0] == board[1][1] == board[2][2] == player or board[0][2] == board[1][1] == board[2][0] == player:
        return True
    return False


def check_draw(board):
    return all(board[i][j] != "" for i in range(3) for j in range(3))


def game_over(message):
    global result_window
    result_window = tk.Toplevel()
    result_window.title("Конец игры")
    center_window(result_window, 400, 200)  # Центрируем окно
    tk.Label(result_window, text=message, font=("Arial", 24), fg="#4CAF50").pack(padx=20, pady=20)
    tk.Button(result_window, text="Новый раунд", command=start_new_game, bg="#4CAF50", fg="white").pack(pady=10)
    tk.Button(result_window, text="Закрыть", command=result_window.quit, bg="#F44336", fg="white").pack(pady=10)


def start_new_game():
    game_window.destroy()
    result_window.destroy()
    start_game_window.deiconify()


def start_game_X():  # Начало игры для крестиков
    global current_player, board, buttons, player_symbol, computer_symbol, game_window
    board = [["" for _ in range(3)] for _ in range(3)]
    player_symbol, computer_symbol, current_player = "X", "O", "X"
    buttons = [[None for _ in range(3)] for _ in range(3)]
    game_window = tk.Toplevel(start_game_window)
    game_window.title("Крестики-нолики: Игра")

    # Размеры кнопок и игрового поля
    button_width = 10
    button_height = 3
    window_width = button_width * 3  # 3 кнопки по горизонтали
    window_height = button_height * 3  # 3 кнопки по вертикали
    center_window(game_window, 600, 400)

    for i in range(3):
        for j in range(3):
            buttons[i][j] = tk.Button(game_window, text="", width=button_width, height=button_height,
                                      font=("Arial", 24),
                                      bg="#e0e0e0", activebackground="#9e9e9e",
                                      command=lambda i=i, j=j: player_turn(i, j))
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)
    start_game_window.withdraw()


def start_game_O():  # Функция для начала игры с ноликами
    global current_player, board, buttons, player_symbol, computer_symbol, game_window
    board = [["" for _ in range(3)] for _ in range(3)]  # Инициализируем поле
    player_symbol = "O"  # Игрок выбирает нолики
    computer_symbol = "X"  # Компьютер будет играть крестиками
    current_player = computer_symbol  # Компьютер ходит первым
    buttons = [[None for _ in range(3)] for _ in range(3)]  # Инициализируем кнопки

    # Создаем игровое окно
    game_window = tk.Toplevel(start_game_window)
    game_window.title("Крестики-нолики: Игра")

    # Размеры кнопок и игрового поля
    button_width = 10
    button_height = 3
    window_width = button_width * 3  # 3 кнопки по горизонтали
    window_height = button_height * 3  # 3 кнопки по вертикали

    center_window(game_window, 600, 400)

    for i in range(3):  # Создание кнопок для игрового поля
        for j in range(3):
            buttons[i][j] = tk.Button(game_window, text="", width=button_width, height=button_height,
                                      font=("Arial", 24),
                                      bg="#e0e0e0", activebackground="#9e9e9e",
                                      command=lambda i=i, j=j: player_turn(i, j))
            buttons[i][j].grid(row=i, column=j, padx=5, pady=5)

    start_game_window.withdraw()  # Закрыть начальное окно выбора
    computer_turn_first()  # После начала игры ходит компьютер первым


def player_turn(i, j):
    global current_player
    if board[i][j] == "":  # Если клетка пуста
        board[i][j] = current_player  # Игрок ставит свой символ
        buttons[i][j].config(text=current_player, state="disabled")  # Отключаем кнопку
        # Проверка на победителя
        if check_winner(board, current_player):
            game_over(f"Игрок ({current_player}) победил!")
            return
        # Проверка на ничью
        if check_draw(board):
            game_over("Ничья!")
            return
        # Переключаем на ход компьютера
        current_player = computer_symbol if current_player == player_symbol else player_symbol
        if current_player == computer_symbol:
            computer_turn()  # Ход компьютера


def computer_turn():  # Функция для хода компьютера
    global current_player
    best_move = None
    best_value = float('-inf')

    # Ищем лучший ход для компьютера
    for i in range(3):
        for j in range(3):
            if board[i][j] == "":
                board[i][j] = computer_symbol
                if check_winner(board, computer_symbol):  # Проверка на победу
                    best_move = (i, j)
                    board[i][j] = ""
                    break
                board[i][j] = ""
    if best_move is None:
        for i in range(3):
            for j in range(3):
                if board[i][j] == "":
                    board[i][j] = player_symbol  # Блокировка хода игрока
                    if check_winner(board, player_symbol):
                        best_move = (i, j)
                        board[i][j] = ""
                        break
                    board[i][j] = ""
    if best_move is None:
        # Если нет блокировки, выбираем случайный ход
        available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
        best_move = random.choice(available_moves)

    # Совершаем лучший ход
    row, col = best_move
    board[row][col] = computer_symbol
    buttons[row][col].config(text=computer_symbol, state="disabled")  # Отключаем кнопку
    # Проверка на победу
    if check_winner(board, computer_symbol):
        game_over(f"Компьютер ({computer_symbol}) победил!")
        return
    # Проверка на ничью
    if check_draw(board):
        game_over("Ничья!")
        return

    # Теперь ходит игрок
    current_player = player_symbol


def computer_turn_first():  # Функция для первого хода компьютера
    global current_player
    available_moves = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ""]
    first_move = random.choice(available_moves)  # Выбираем случайную клетку для первого хода
    row, col = first_move
    board[row][col] = computer_symbol
    buttons[row][col].config(text=computer_symbol, state="disabled")  # Отключаем кнопку
    current_player = player_symbol  # Теперь ходит игрок


# Начальное окно выбора
start_game_window = tk.Tk()
start_game_window.title("Крестики-нолики")
center_window(start_game_window, 300, 200)

tk.Label(start_game_window, text="Выберите символ:", font=("Arial", 16)).pack(pady=10)
tk.Button(start_game_window, text="X", width=10, height=2, font=("Arial", 16), command=start_game_X, bg="#4CAF50",
          fg="white").pack(pady=5)
tk.Button(start_game_window, text="O", width=10, height=2, font=("Arial", 16), command=start_game_O, bg="#F44336",
          fg="white").pack(pady=5)

start_game_window.mainloop()
