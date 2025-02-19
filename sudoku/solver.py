import random
from collections import defaultdict

class TreeSearchSudokuSolver:
    def __init__(self, board):
        self.board = board
        self.memory = []  # Stores past moves
        self.history = []  # Tracks paths explored
        self.thoughts = []  # Logs the decision process

    def is_valid(self, row, col, num):
        """Check if placing 'num' at 'board[row][col]' follows Sudoku rules."""
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty_location(self):
        """Find the first empty cell in the board (0 represents empty)."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def score_moves(self, row, col):
        """
        Rank possible numbers (1-9) for a given cell.
        Scores are based on how often a number appears in row, column, and grid.
        """
        frequency = defaultdict(int)
        for x in range(9):
            if self.board[row][x] != 0:
                frequency[self.board[row][x]] += 1
            if self.board[x][col] != 0:
                frequency[self.board[x][col]] += 1
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] != 0:
                    frequency[self.board[i + start_row][j + start_col]] += 1

        # Score lower-frequency numbers higher (prefer less common choices)
        candidates = [(num, frequency[num]) for num in range(1, 10) if self.is_valid(row, col, num)]
        candidates.sort(key=lambda x: x[1])  # Sort by lowest frequency

        return [num for num, _ in candidates]

    def solve(self):
        """Tree-of-Thought approach: Explore multiple move options with backtracking."""
        empty = self.find_empty_location()
        if not empty:
            return True  # Puzzle solved

        row, col = empty
        candidates = self.score_moves(row, col)  # Get ranked move options

        for num in candidates:
            self.board[row][col] = num
            self.history.append((row, col, num))
            self.thoughts.append(f"Placing {num} at ({row}, {col})")

            if self.solve():  # Recursive step
                return True  # Success

            # Backtrack if the path failed
            self.board[row][col] = 0
            self.history.pop()
            self.thoughts.append(f"Backtracking at ({row}, {col}), removing {num}")

        return False  # No solution found in this path

    def print_thoughts(self):
        """Print the reasoning steps taken by the solver."""
        print("\n".join(self.thoughts))

    def solve_with_tot(self, max_steps=100):
        """Attempt solving using ToT principles with a step limit."""
        for _ in range(max_steps):
            if self.solve():
                return self.to_string()
            self.backtrack()  # If stuck, backtrack to explore other options
        return "Failed to solve"

    def backtrack(self):
        """Backtrack to the last decision point and try a different path."""
        if not self.history:
            return
        row, col, num = self.history.pop()
        self.board[row][col] = 0
        self.thoughts.append(f"Backtracking deeper: Removed {num} at ({row}, {col})")
        self.backtrack()  # Continue backtracking if needed

    def to_string(self):
        """Convert the board to a string for easy visualization."""
        return '\n'.join([' '.join(str(cell) for cell in row) for row in self.board])


class BacktrackingSudokuSolver:
    def __init__(self, board):
        self.board = board
        self.memory = []  # Stores past moves
        self.history = []  # Tracks paths explored
        self.thoughts = []  # Logs the decision process

    def is_valid(self, row, col, num):
        """Check if placing 'num' at 'board[row][col]' follows Sudoku rules."""
        for x in range(9):
            if self.board[row][x] == num or self.board[x][col] == num:
                return False
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] == num:
                    return False
        return True

    def find_empty_location(self):
        """Find the first empty cell in the board (0 represents empty)."""
        for i in range(9):
            for j in range(9):
                if self.board[i][j] == 0:
                    return (i, j)
        return None

    def score_moves(self, row, col):
        """
        Rank possible numbers (1-9) for a given cell.
        Scores are based on how often a number appears in row, column, and grid.
        """
        frequency = defaultdict(int)
        for x in range(9):
            if self.board[row][x] != 0:
                frequency[self.board[row][x]] += 1
            if self.board[x][col] != 0:
                frequency[self.board[x][col]] += 1
        
        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if self.board[i + start_row][j + start_col] != 0:
                    frequency[self.board[i + start_row][j + start_col]] += 1

        # Score lower-frequency numbers higher (prefer less common choices)
        candidates = [(num, frequency[num]) for num in range(1, 10) if self.is_valid(row, col, num)]
        candidates.sort(key=lambda x: x[1])  # Sort by lowest frequency

        return [num for num, _ in candidates]

    def solve(self):
        """Tree-of-Thought approach: Explore multiple move options with backtracking."""
        empty = self.find_empty_location()
        if not empty:
            return True  # Puzzle solved

        row, col = empty
        candidates = self.score_moves(row, col)  # Get ranked move options

        for num in candidates:
            self.board[row][col] = num
            self.history.append((row, col, num))
            self.thoughts.append(f"Placing {num} at ({row}, {col})")

            if self.solve():  # Recursive step
                return True  # Success

            # Backtrack if the path failed
            self.board[row][col] = 0
            self.history.pop()
            self.thoughts.append(f"Backtracking at ({row}, {col}), removing {num}")

        return False  # No solution found in this path

    def print_thoughts(self):
        """Print the reasoning steps taken by the solver."""
        print("\n".join(self.thoughts))

    def solve_with_tot(self, max_steps=100):
        """Attempt solving using ToT principles with a step limit."""
        for _ in range(max_steps):
            if self.solve():
                return self.to_string()
            self.backtrack()  # If stuck, backtrack to explore other options
        return "Failed to solve"

    def backtrack(self):
        """Backtrack to the last decision point and try a different path."""
        if not self.history:
            return
        row, col, num = self.history.pop()
        self.board[row][col] = 0
        self.thoughts.append(f"Backtracking deeper: Removed {num} at ({row}, {col})")
        self.backtrack()  # Continue backtracking if needed

    def to_string(self):
        """Convert the board to a string for easy visualization."""
        return '\n'.join([' '.join(str(cell) for cell in row) for row in self.board])




if __name__ == "__main__":
        
    # Example Usage
    board = [
        [5, 3, 0, 0, 7, 0, 0, 0, 0],
        [6, 0, 0, 1, 9, 5, 0, 0, 0],
        [0, 9, 8, 0, 0, 0, 0, 6, 0],
        [8, 0, 0, 0, 6, 0, 0, 0, 3],
        [4, 0, 0, 8, 0, 3, 0, 0, 1],
        [7, 0, 0, 0, 2, 0, 0, 0, 6],
        [0, 6, 0, 0, 0, 0, 2, 8, 0],
        [0, 0, 0, 4, 1, 9, 0, 0, 5],
        [0, 0, 0, 0, 8, 0, 0, 7, 9]
    ]

    solver = TreeSearchSudokuSolver(board)
    solution = solver.solve_with_tot()
    solver.print_thoughts()  # Print reasoning process
    print("TreeSearch solution:\n", solution)


    
    
    solver = BacktrackingSudokuSolver(board)
    solution = solver.solve_with_tot()
    solver.print_thoughts()  # Print reasoning process
    print("Backtracking solution:\n", solution)