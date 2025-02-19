
# sudoku_gui.py

import tkinter as tk
from tkinter import messagebox
from sudoku.generator import SudokuGenerator

class SudokuApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sudoku Game")
        
        self.difficulty = tk.StringVar(value="medium")
        self.generator = SudokuGenerator(self.difficulty.get())
        self.board = self.generator.generate_sudoku()
        self.solution = self.generator.solution
        
        self.cells = []
        self.create_ui()
    
    def create_ui(self):
        # Difficulty selection
        difficulty_frame = tk.Frame(self.root)
        difficulty_frame.pack()
        tk.Label(difficulty_frame, text="Difficulty:").pack(side=tk.LEFT)
        for level in ["very easy", "easy", "medium", "hard", "expert"]:
            tk.Radiobutton(difficulty_frame, text=level.capitalize(), variable=self.difficulty, value=level, command=self.new_game).pack(side=tk.LEFT)
        
        # Sudoku Grid
        grid_frame = tk.Frame(self.root)
        grid_frame.pack()
        for i in range(9):
            row = []
            for j in range(9):
                entry = tk.Entry(grid_frame, width=4, font=("Arial", 18), justify="center")
                entry.grid(row=i, column=j, padx=2, pady=2)
                if self.board[i][j] != 0:
                    entry.insert(0, str(self.board[i][j]))
                    entry.config(state="disabled")
                row.append(entry)
            self.cells.append(row)
        
        # Buttons in a 2x2 grid
        button_frame = tk.Frame(self.root)
        button_frame.pack()
        
        tk.Button(button_frame, text="New Game", command=self.new_game, width=10, height=2).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Check Solution", command=self.check_solution, width=10, height=2).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="Show Solution", command=self.show_solution, width=10, height=2).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="Reset", command=self.reset_board, width=10, height=2).grid(row=1, column=1, padx=5, pady=5)
    
    def new_game(self):
        self.generator = SudokuGenerator(self.difficulty.get())
        self.board = self.generator.generate_sudoku()
        self.solution = self.generator.solution
        self.update_board()
    
    def update_board(self):
        for i in range(9):
            for j in range(9):
                self.cells[i][j].config(state="normal")
                self.cells[i][j].delete(0, tk.END)
                if self.board[i][j] != 0:
                    self.cells[i][j].insert(0, str(self.board[i][j]))
                    self.cells[i][j].config(state="disabled")
    
    def check_solution(self):
        for i in range(9):
            for j in range(9):
                if self.cells[i][j].get().isdigit():
                    if int(self.cells[i][j].get()) != self.solution[i][j]:
                        messagebox.showerror("Error", "Incorrect solution!")
                        return
                else:
                    messagebox.showerror("Error", "Some cells are empty!")
                    return
        messagebox.showinfo("Success", "Correct solution!")
    
    def show_solution(self):
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    self.cells[i][j].config(fg="blue")
                    self.cells[i][j].delete(0, tk.END)
                    self.cells[i][j].insert(0, str(self.solution[i][j]))
    
    def reset_board(self):
        self.update_board()

if __name__ == "__main__":
    root = tk.Tk()
    app = SudokuApp(root)
    root.mainloop()
