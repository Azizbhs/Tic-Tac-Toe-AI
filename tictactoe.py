import tkinter
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
        
        # Check for win or draw after the player's move
        if check_winner():
            label.config(text=f"{current_player} wins!")
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            disable_buttons()
        elif check_draw():
            label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
        else:
            # Switch to the other player
            switch_player()
            # If it's the bot's turn, call bot_move
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

def evaluate_board(state):
    """
    Assigns a score based on whether player1 or player2 wins in the current state.
    """
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
    
    # If it's the bot's first move, prioritize the center or a random corner
    if is_bot_first_move:
        is_bot_first_move = False
        if board[1][1]['text'] == ' ':
            board[1][1]['text'] = player2
            board[1][1]['foreground'] = 'red'  # Set bot color
        else:
            board[0][0]['text'] = player2
            board[0][0]['foreground'] = 'red'  # Set bot color

        # Check for win or draw after this immediate move
        if check_winner():
            label.config(text=f"{player2} wins!")
            messagebox.showinfo("Game Over", f"Player {player2} wins!")
            disable_buttons()
        elif check_draw():
            label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
        else:
            switch_player()  # Pass turn back to the player
        return  # Exit after taking the center

    # If center is not available, proceed with minimax as usual
    best_score = -1000
    move = (-1, -1)

    for row in range(3):
        for col in range(3):
            if board[row][col]['text'] == ' ':
                # Simulate bot move
                board[row][col]['text'] = player2
                score = minimax(board, 0, False)  # Start minimax with player's turn
                board[row][col]['text'] = ' '  # Undo move
                
                # Update best move if the score is higher
                if score > best_score:
                    best_score = score
                    move = (row, col)

    # Make the best move for the bot
    if move != (-1, -1):
        row, col = move
        board[row][col]['text'] = player2
        board[row][col]['foreground'] = 'red'  # Set bot color

    # Check if the bot's move resulted in a win or draw
    if check_winner():
        label.config(text=f"{player2} wins!")
        messagebox.showinfo("Game Over", f"Player {player2} wins!")
        disable_buttons()
    elif check_draw():
        label.config(text="It's a draw!")
        messagebox.showinfo("Game Over", "It's a draw!")
        disable_buttons()
    else:
        switch_player()  # Pass turn back to the player
        
def run_game(player_symbol, difficulty):
    global player1, player2, current_player, board, window, label
    player1, player2 = ('X', 'O') if player_symbol == 'X' else ('O', 'X')
    current_player = player1
    board = [[None, None, None], [None, None, None], [None, None, None]]

    window = tkinter.Tk()
    window.title('Tic-Tac-Toe')
    window.resizable(0, 0)

    frame = tkinter.Frame(window)
    frame.grid(row=0, column=0, padx=10, pady=10)

    # Label for current player
    label = tkinter.Label(frame, text=f"{current_player}'s turn", font=('Courier New', 20), foreground='black')
    label.grid(row=0, column=0, columnspan=3)

    # Create the Tic-Tac-Toe board buttons
    for row in range(3):
        for col in range(3):
            board[row][col] = tkinter.Button(
                frame, text=' ', font=('Arial', 40, "bold"), height=2, width=5, background='white',
                command=lambda row=row, col=col: on_click(row, col)
            )
            board[row][col].grid(row=row+1, column=col)  # Button rows start from row 1

    # Restart and Back buttons
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

    window.mainloop()
