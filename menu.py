import tkinter as tk
from tkinter import messagebox
import random
import tictactoe  

def start_game():
    global player_symbol, difficulty
    if difficulty.get() == "":
        messagebox.showerror("Selection Error", "Please choose a difficulty level.")
        return
    
    player_symbol = random.choice(['X', 'O'])  
    messagebox.showinfo("Symbol Assigned", f"You will play as '{player_symbol}'")


    tictactoe.run_game(player_symbol, difficulty.get())  
    window.destroy()  


window = tk.Tk()
window.title("Tic-Tac-Toe Menu")
window.geometry("400x300")
window.resizable(0, 0)


frame = tk.Frame(window, background="white")
frame.pack(expand=True, fill="both")

label = tk.Label(frame, text="Choose Bot Difficulty", font=('Courier New', 20), background="white")
label.pack(pady=10)

difficulty = tk.StringVar(value="normal")

tk.Radiobutton(frame, text="Easy", font=('Courier New', 15), variable=difficulty, value="easy", background="white").pack(anchor="w", padx=20)
tk.Radiobutton(frame, text="Normal", font=('Courier New', 15), variable=difficulty, value="normal", background="white").pack(anchor="w", padx=20)
tk.Radiobutton(frame, text="Impossible", font=('Courier New', 15), variable=difficulty, value="impossible", background="white").pack(anchor="w", padx=20)

start_button = tk.Button(frame, text="Start Game", font=('Courier New', 20), command=start_game)
start_button.pack(pady=20)

window.update_idletasks()
width = window.winfo_width()
height = window.winfo_height()
x = (window.winfo_screenwidth() // 2) - (width // 2)
y = (window.winfo_screenheight() // 2) - (height // 2)
window.geometry(f'{width}x{height}+{x}+{y}')

window.mainloop()