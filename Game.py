import random
import tkinter as tk
from tkinter import messagebox

class Cell:
    def __init__(self):
        self.is_mine = False
        self.is_revealed = False
        self.is_flagged = False
        self.adjacent_mines = 0

class MinesweeperGUI:
    def __init__(self, rows, cols, num_mines):
        self.rows = rows
        self.cols = cols
        self.num_mines = num_mines
        self.num_cells = rows * cols
        self.board = [[Cell() for _ in range(cols)] for _ in range(rows)]
        self.root = tk.Tk()
        self.buttons = [[None for _ in range(cols)] for _ in range(rows)]
        self.create_menu()
        self.create_board()

    def create_menu(self):
        menubar = tk.Menu(self.root)
        game_menu = tk.Menu(menubar, tearoff=0)
        game_menu.add_command(label="Restart", command=self.restart_game)
        game_menu.add_command(label="Exit", command=self.root.destroy)
        menubar.add_cascade(label="Game", menu=game_menu)
        self.root.config(menu=menubar)

    def create_board(self):
        self.root.title("Minesweeper")
        for row in range(self.rows):
            for col in range(self.cols):
                button = tk.Button(
                    self.root,
                    width=3,
                    height=1,
                    relief=tk.RAISED,
                    command=lambda r=row, c=col: self.on_left_click(r, c)
                )
                button.bind("<Button-3>", lambda event, r=row, c=col: self.on_right_click(event, r, c))
                button.grid(row=row, column=col)
                self.buttons[row][col] = button

    def place_mines(self, start_row, start_col):
        mines_placed = 0
        while mines_placed < self.num_mines:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            if not self.board[row][col].is_mine and (row != start_row or col != start_col):
                self.board[row][col].is_mine = True
                mines_placed += 1

    def calculate_adjacent_mines(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if cell.is_mine:
                    continue
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i == 0 and j == 0:
                            continue
                        new_row, new_col = row + i, col + j
                        if 0 <= new_row < self.rows and 0 <= new_col < self.cols and self.board[new_row][new_col].is_mine:
                            cell.adjacent_mines += 1

    def reveal_cell(self, row, col):
        cell = self.board[row][col]
        button = self.buttons[row][col]
        if cell.is_revealed or cell.is_flagged:
            return
        cell.is_revealed = True
        button.configure(relief=tk.SUNKEN)
        if cell.is_mine:
            # Game over condition
            self.game_over()
        elif cell.adjacent_mines == 0:
            # Auto-reveal adjacent cells if the current cell has no adjacent mines
            for i in range(-1, 2):
                for j in range(-1, 2):
                    new_row, new_col = row + i, col + j
                    if 0 <= new_row < self.rows and 0 <= new_col < self.cols:
                        self.reveal_cell(new_row, new_col)
        else:
            button.configure(text=str(cell.adjacent_mines))

        if self.check_game_won():
            self.game_won()

    def flag_cell(self, row, col):
        cell = self.board[row][col]
        button = self.buttons[row][col]
        if cell.is_revealed:
            return
        if cell.is_flagged:
            cell.is_flagged = False
            button.configure(text="")
        else:
            cell.is_flagged = True
            button.configure(text="F")

    def game_over(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col].configure(state=tk.DISABLED)
        messagebox.showinfo("Game Over", "You hit a mine!")

    def restart_game(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.board[row][col] = Cell()
                self.buttons[row][col].configure(text="", state=tk.NORMAL, relief=tk.RAISED)
        self.place_mines(0, 0)
        self.calculate_adjacent_mines()

    def check_game_won(self):
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.board[row][col]
                if not cell.is_mine and not cell.is_revealed:
                    return False
        return True

    def game_won(self):
        for row in range(self.rows):
            for col in range(self.cols):
                self.buttons[row][col].configure(state=tk.DISABLED)
        messagebox.showinfo("Congratulations", "You cleared the board!")

    def on_left_click(self, row, col):
        self.reveal_cell(row, col)

    def on_right_click(self, event, row, col):
        self.flag_cell(row, col)

# Example usage
rows = 8
cols = 8
num_mines = 10

minesweeper = MinesweeperGUI(rows, cols, num_mines)
minesweeper.place_mines(0, 0)  # Start position, pass the desired starting row and column
minesweeper.calculate_adjacent_mines()
minesweeper.root.mainloop()
