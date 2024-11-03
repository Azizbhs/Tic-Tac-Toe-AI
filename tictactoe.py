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
        if check_winner():
            label.config(text=f"{current_player} wins!")
            messagebox.showinfo("Game Over", f"Player {current_player} wins!")
            disable_buttons()
        elif check_draw():
            label.config(text="It's a draw!")
            messagebox.showinfo("Game Over", "It's a draw!")
            disable_buttons()
        else:
            switch_player()

def switch_player():
    global current_player
    current_player = player1 if current_player == player2 else player2
    label.config(text=f"{current_player}'s turn")

def check_winner():
    for i in range(3):
        # Check rows for winner
        if board[i][0]['text'] == board[i][1]['text'] == board[i][2]['text'] != ' ':
            return True
        # Check columns for winner
        if board[0][i]['text'] == board[1][i]['text'] == board[2][i]['text'] != ' ':
            return True
    # Check diagonals for winner
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
    global current_player
    current_player = player1
    label.config(text=f"{current_player}'s turn")
    for row in range(3):
        for col in range(3):
            board[row][col]['text'] = ' '
            board[row][col]['state'] = 'normal'

def go_back():
    window.destroy()  # Closes the game window

def run_game(player_symbol, difficulty):
    # Assign values to global variables
    global player1, player2, current_player, board, window, label
    player1, player2 = ('X', 'O') if player_symbol == 'X' else ('O', 'X')
    current_player = player1
    board = [[None, None, None], [None, None, None], [None, None, None]]

    # Set up the game window
    window = tkinter.Tk()
    window.title('Tic-Tac-Toe')
    window.resizable(0, 0)

    # Game layout
    frame = tkinter.Frame(window)
    frame.grid(row=0, column=0, padx=10, pady=10)  # Use grid instead of pack

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
