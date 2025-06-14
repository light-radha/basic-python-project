import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic-Tac-Toe")

        self.current_player = 'X'
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.buttons = [[None for _ in range(3)] for _ in range(3)]

        self.x_wins = 0
        self.o_wins = 0
        self.draws = 0

        self.create_widgets()
        self.update_status()

    def create_widgets(self):
        self.status_label = tk.Label(self.root, text="", font=("Arial", 14))
        self.status_label.grid(row=0, column=0, columnspan=3, pady=10)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(self.root, text=" ", font=("Arial", 24), width=5, height=2,
                                command=lambda r=i, c=j: self.on_button_click(r, c))
                btn.grid(row=i+1, column=j)
                self.buttons[i][j] = btn

        self.score_label = tk.Label(self.root, text="", font=("Arial", 12))
        self.score_label.grid(row=4, column=0, columnspan=3, pady=10)

        self.reset_button = tk.Button(self.root, text="Reset Game", command=self.reset_board)
        self.reset_button.grid(row=5, column=0, columnspan=3, pady=5)

    def on_button_click(self, row, col):
        if self.board[row][col] == ' ':
            self.board[row][col] = self.current_player
            self.buttons[row][col].config(text=self.current_player, state="disabled")
            if self.check_win(self.current_player):
                messagebox.showinfo("Game Over", f"Player {self.current_player} wins!")
                if self.current_player == 'X':
                    self.x_wins += 1
                else:
                    self.o_wins += 1
                self.update_score()
                self.disable_all_buttons()
            elif self.is_board_full():
                messagebox.showinfo("Game Over", "It's a draw!")
                self.draws += 1
                self.update_score()
                self.disable_all_buttons()
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
                self.update_status()

    def check_win(self, player):
        # Check rows and columns
        for i in range(3):
            if all(self.board[i][j] == player for j in range(3)) or \
               all(self.board[j][i] == player for j in range(3)):
                return True
        # Check diagonals
        if (self.board[0][0] == player and self.board[1][1] == player and self.board[2][2] == player) or \
           (self.board[0][2] == player and self.board[1][1] == player and self.board[2][0] == player):
            return True
        return False

    def is_board_full(self):
        return all(cell != ' ' for row in self.board for cell in row)

    def disable_all_buttons(self):
        for row in self.buttons:
            for btn in row:
                btn.config(state="disabled")

    def reset_board(self):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        for row in self.buttons:
            for btn in row:
                btn.config(text=" ", state="normal")
        self.update_status()

    def update_status(self):
        self.status_label.config(text=f"Player {self.current_player}'s turn")

    def update_score(self):
        self.score_label.config(text=f"Score - X: {self.x_wins}  O: {self.o_wins}  Draws: {self.draws}")

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
