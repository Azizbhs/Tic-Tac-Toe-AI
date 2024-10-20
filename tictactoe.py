import tkinter
from tkinter import messagebox

def on_click(row, col):
    global current_player
    if board[row][col]['text'] == ' ' and not check_winner():  # Ensure spot is empty and game not over
        board[row][col]['text'] = current_player
        board[row][col]['foreground'] = 'blue' if current_player == 'X' else 'red'  # X is blue, O is red
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
    # Check rows, columns, and diagonals for a win
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
    global current_player
    current_player = player1
    label.config(text=f"{current_player}'s turn")
    for row in range(3):
        for col in range(3):
            board[row][col]['text'] = ' '
            board[row][col]['state'] = 'normal'

def go_back():
    window.destroy()  # Close the game window for now; you can add a menu later

player1 = 'X'
player2 = 'O'
current_player = player1
board = [[None, None, None], [None, None, None], [None, None, None]]

window = tkinter.Tk()
window.title('Tic-Tac-Toe')
window.resizable(0, 0)

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text=current_player+"'s turn", font=('Courier New', 20), foreground='black')

label.pack()
frame.pack()

label.grid(row=0, column=0, columnspan=3)

for row in range(3):
    for col in range(3):
        board[row][col] = tkinter.Button(frame, text=' ', font=('Arial', 40, "bold"), height=2, width=5, background='white', command=lambda row=row, col=col: on_click(row, col))
        board[row][col].grid(row=row+1, column=col)

# Add Restart and Back buttons in the same row with 50/50 space
restart_button = tkinter.Button(frame, text='Restart', font=('Courier New', 20), foreground='black', command=reset_game)
restart_button.grid(row=4, columnspan=3, sticky='ew')

back_button = tkinter.Button(frame, text='Back', font=('Courier New', 20), foreground='black', command=go_back)
back_button.grid(row=5, columnspan=3, sticky='ew')

window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f'{width}x{height}+{x}+{y}')

window.mainloop()