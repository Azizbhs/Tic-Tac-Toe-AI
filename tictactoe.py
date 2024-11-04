import tkinter
import random
from tkinter import messagebox

# Global variable declarations
player1 = None
player2 = None
current_player = None
board = None
window = None
label = None

def on_click(row, col):
    global current_player
    if board[row][col]['text'] == ' ' and not check_winner():
        board[row][col]['text'] = current_player
        board[row][col]['foreground'] = 'blue' if current_player == 'X' else 'red'
        
        if check_winner():
            end_game(current_player)
        elif check_draw():
           end_game()
        else:
            switch_player()
            if current_player == player2:
                bot_move()

def switch_player():
    global current_player
    current_player = player1 if current_player == player2 else player2
    label.config(text=f"{current_player}'s turn")

def check_winner():
    for i in range(3):
        if board[i][0]['text'] == board[i][1]['text'] == board[i][2]['text'] != ' ':
            return True
        if board[0][i]['text'] == board[1][i]['text'] == board[2][i]['text'] != ' ':
            return True
    if board[0][0]['text'] == board[1][1]['text'] == board[2][2]['text'] != ' ':
        return True
    if board[0][2]['text'] == board[1][1]['text'] == board[2][0]['text'] != ' ':
        return True
    return False

def check_draw():
    for row in range(3):
        for col in range(3):
            if board[row][col]['text'] == ' ':
                return False
    return True

def disable_buttons():
    for row in range(3):
        for col in range(3):
            board[row][col]['state'] = 'disabled'

def reset_game():
    global current_player,is_bot_first_move
    is_bot_first_move = True
    current_player = player1
    label.config(text=f"{current_player}'s turn")
    for row in range(3):
        for col in range(3):
            board[row][col]['text'] = ' '
            board[row][col]['state'] = 'normal'

def go_back():
    window.destroy()  

def end_game(winner=None):
    if winner:
        label.config(text=f"{winner} wins!")
        messagebox.showinfo("Game Over", f"Player {winner} wins!")
    else:
        label.config(text="It's a draw!")
        messagebox.showinfo("Game Over", "It's a draw!")
    disable_buttons()

def evaluate_board(state):
    for i in range(3):
        if state[i][0]['text'] == state[i][1]['text'] == state[i][2]['text'] != ' ':
            return 1 if state[i][0]['text'] == player2 else -1
        if state[0][i]['text'] == state[1][i]['text'] == state[2][i]['text'] != ' ':
            return 1 if state[0][i]['text'] == player2 else -1
    if state[0][0]['text'] == state[1][1]['text'] == state[2][2]['text'] != ' ':
        return 1 if state[0][0]['text'] == player2 else -1
    if state[0][2]['text'] == state[1][1]['text'] == state[2][0]['text'] != ' ':
        return 1 if state[0][2]['text'] == player2 else -1
    return 0

def random_move():
    empty_cells = [(row, col) for row in range(3) for col in range(3) if board[row][col]['text'] == ' ']
    row, col = random.choice(empty_cells)
    board[row][col]['text'] = player2
    board[row][col]['foreground'] = 'blue' if player2 == 'X' else 'red'

def minimax(state, depth, is_maximizing):
    score = evaluate_board(state)
    if score == 1 or score == -1:
        return score
    if check_draw():
        return 0

    if is_maximizing:
        return maximize(state, depth)
    else:
        return minimize(state, depth)

def maximize(state, depth):
    best_score = -1000
    for row in range(3):
        for col in range(3):
            if state[row][col]['text'] == ' ':
                state[row][col]['text'] = player2
                score = minimax(state, depth + 1, False)
                state[row][col]['text'] = ' '
                best_score = max(score, best_score)
    return best_score

def minimize(state, depth):
    best_score = 1000
    for row in range(3):
        for col in range(3):
            if state[row][col]['text'] == ' ':
                state[row][col]['text'] = player1
                score = minimax(state, depth + 1, True)
                state[row][col]['text'] = ' '
                best_score = min(score, best_score)
    return best_score

is_bot_first_move = True

def bot_move():
    global is_bot_first_move
    if is_bot_first_move:
        is_bot_first_move = False
        if board[1][1]['text'] == ' ':
            board[1][1]['text'] = player2
            board[1][1]['foreground'] = 'blue' if player2 == 'X' else 'red'
        else:
            corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
            row, col = random.choice(corners)
            board[row][col]['text'] = player2
            board[row][col]['foreground'] = 'blue' if player2 == 'X' else 'red'
        if check_winner():
            end_game(player2)
        elif check_draw():
            end_game()
        else:
            switch_player() 
        return 

    if difficulty == "easy" or (difficulty == "normal" and random.random() <= 0.4):
        #Choose any random empty cell
        random_move()
    else:
        # Impossible or 60% chance for "normal" difficulty
        best_score = -1000
        move = (-1, -1)
        for row in range(3):
            for col in range(3):
                if board[row][col]['text'] == ' ':
                    board[row][col]['text'] = player2
                    score = minimax(board, 0, False)
                    board[row][col]['text'] = ' ' 
                    if score > best_score:
                        best_score = score
                        move = (row, col)
        if move != (-1, -1):
            row, col = move
            board[row][col]['text'] = player2
            board[row][col]['foreground'] = 'blue' if player2 == 'X' else 'red'

    if check_winner():
        end_game(player2)
    elif check_draw():
        end_game()
    else:
        switch_player() 
        
def run_game(player_symbol, selected_difficulty):
    global player1, player2, current_player, board, window, label, is_bot_first_move, difficulty
    player1, player2 = ('X', 'O') if player_symbol == 'X' else ('O', 'X')
    current_player = 'X' 
    is_bot_first_move = True
    difficulty = selected_difficulty
    board = [[None, None, None], [None, None, None], [None, None, None]]

    window = tkinter.Tk()
    window.title('Tic-Tac-Toe')
    window.resizable(0, 0)

    frame = tkinter.Frame(window)
    frame.grid(row=0, column=0, padx=10, pady=10)

    label = tkinter.Label(frame, text=f"{current_player}'s turn", font=('Courier New', 20), foreground='black')
    label.grid(row=0, column=0, columnspan=3)

    for row in range(3):
        for col in range(3):
            board[row][col] = tkinter.Button(
                frame, text=' ', font=('Arial', 40, "bold"), height=2, width=5, background='white',
                command=lambda row=row, col=col: on_click(row, col)
            )
            board[row][col].grid(row=row+1, column=col) 

    restart_button = tkinter.Button(frame, text='Restart', font=('Courier New', 20), foreground='black', command=reset_game)
    restart_button.grid(row=4, column=0, columnspan=3, sticky='ew', pady=(10, 0))

    back_button = tkinter.Button(frame, text='Back', font=('Courier New', 20), foreground='black', command=go_back)
    back_button.grid(row=5, column=0, columnspan=3, sticky='ew')

    # Center the window on the screen
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'{width}x{height}+{x}+{y}')

    if player2 == 'X':
        bot_move()

    window.mainloop()
