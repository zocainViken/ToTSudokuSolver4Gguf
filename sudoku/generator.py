import random
import copy

class SudokuGenerator:
    def __init__(self, difficulty="medium"):
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.solution = None  # Store the full solution
        self.difficulty_levels = {
            "very easy": 25,  # Fewer empty cells
            "easy": 30,
            "medium": 40,
            "hard": 50,
            "expert": 55  # More empty cells, harder puzzle
        }
        self.empty_cells = self.difficulty_levels.get(difficulty, 40)

    def is_valid(self, board, row, col, num):
        """Check if num can be placed at board[row][col]."""
        for x in range(9):
            if board[row][x] == num or board[x][col] == num:
                return False

        start_row, start_col = 3 * (row // 3), 3 * (col // 3)
        for i in range(3):
            for j in range(3):
                if board[i + start_row][j + start_col] == num:
                    return False
        return True

    def solve(self, board):
        """Backtracking solver to generate a valid Sudoku solution."""
        empty = self.find_empty_location(board)
        if not empty:
            return True
        row, col = empty

        nums = list(range(1, 10))
        random.shuffle(nums)  # Randomize number selection
        for num in nums:
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                if self.solve(board):
                    return True
                board[row][col] = 0

        return False

    def find_empty_location(self, board):
        """Find an empty cell (0) on the board."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return (i, j)
        return None

    def generate_full_board(self):
        """Create a fully solved valid Sudoku board."""
        self.solve(self.board)
        self.solution = copy.deepcopy(self.board)  # Store a copy of the full solution

    def count_solutions(self, board):
        """Count the number of solutions a Sudoku board has."""
        board_copy = copy.deepcopy(board)
        return self._count_solutions_helper(board_copy)

    def _count_solutions_helper(self, board):
        """Recursive helper to count solutions."""
        empty = self.find_empty_location(board)
        if not empty:
            return 1  # Found a valid solution

        row, col = empty
        count = 0

        for num in range(1, 10):
            if self.is_valid(board, row, col, num):
                board[row][col] = num
                count += self._count_solutions_helper(board)
                if count > 1:  # Stop early if more than one solution exists
                    return count
                board[row][col] = 0

        return count

    def remove_numbers(self):
        """Remove numbers while ensuring a unique solution."""
        attempts = self.empty_cells
        while attempts > 0:
            row, col = random.randint(0, 8), random.randint(0, 8)
            while self.board[row][col] == 0:  # Ensure we remove an actual number
                row, col = random.randint(0, 8), random.randint(0, 8)

            backup = self.board[row][col]
            self.board[row][col] = 0

            # Check if the puzzle still has a unique solution
            if self.count_solutions(self.board) != 1:
                self.board[row][col] = backup  # Restore if removing makes it ambiguous
            else:
                attempts -= 1

    def generate_sudoku(self):
        """Create a full Sudoku board, then remove numbers to make a puzzle."""
        self.generate_full_board()
        self.remove_numbers()
        return self.board

    def print_board(self, board=None, title="Generated Sudoku Puzzle"):
        """Print the Sudoku board in a readable format."""
        board = board or self.board
        print(f"\n{title}:")
        for row in board:
            print(" ".join(str(num) if num != 0 else "*" for num in row))

    def solution_board(self):
        """Return or print the full solution before numbers were removed."""
        if self.solution:
            self.print_board(self.solution, title="Solution Board")
        else:
            print("No solution available. Generate a puzzle first.")


if __name__ == '__main__':
    # Example Usage
    generator = SudokuGenerator(difficulty="hard")
    sudoku_puzzle = generator.generate_sudoku()
    generator.print_board()

    print("\nShowing Solution:")
    generator.solution_board()
