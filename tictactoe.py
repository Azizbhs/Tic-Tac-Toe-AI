import tkinter

def on_click(row, col):
    # TODO document why this method is empty
    pass

def go_back():
    # TODO document why this method is empty
    pass

player1 = 'X'
player2 = 'O'
current_player = player1
board = [[0,0,0],[0,0,0],[0,0,0]]


window = tkinter.Tk()
window.title('Tic-Tac-Toe')
window.resizable(0, 0)

frame = tkinter.Frame(window)
label = tkinter.Label(frame, text= current_player+"'s turn", font=('Courier New', 20),foreground='black')

label.pack()
frame.pack()

label.grid(row=0, column=0, columnspan=3)

for row in range(3):
    for col in range(3):
        board[row][col] = tkinter.Button(frame, text=' ', font=('Arial', 40, "bold"), height=2, width=5, background= 'white', foreground='purple', command=lambda row=row, col=col: on_click(row, col))
        board[row][col].grid(row=row+1, column=col)

button = tkinter.Button(frame, text='Main menu', font=('Courier New', 20), foreground='black', command=go_back)

button.grid(row=4, column=0, columnspan=3, sticky='ew')

window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f'{width}x{height}+{x}+{y}')

window.mainloop()

