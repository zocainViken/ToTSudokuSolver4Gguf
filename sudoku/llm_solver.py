import copy
import re
from llama_cpp import Llama
from config import MODEL_PATH

llm = Llama(
    MODEL_PATH,
    chat_format='chat-format',
    n_batch=4096,
    n_ctx=4096,
    max_tokens = 4096,# None unlimited tokens
    verbose = False)


class TreeNode:
    """Node in the search tree representing a partially solved Sudoku board."""
    def __init__(self, board, parent=None):
        self.board = copy.deepcopy(board)  # Deep copy to avoid mutation
        self.children = []
        self.parent = parent

    def add_child(self, board):
        """Create and return a new child node."""
        child = TreeNode(board, parent=self)
        self.children.append(child)
        return child

class ToTController:
    """Manages backtracking and stopping criteria."""
    def should_backtrack(self, node):
        """Decide if we need to backtrack based on ToT rules."""
        if not is_valid_sudoku(node.board):  # Invalid board
            return True
        if len(node.children) > 5:  # Too many failed attempts
            return True
        return False

def is_valid_sudoku(board):
    """Check if the board follows Sudoku rules (row, col, and 3x3 grid)."""
    for i in range(9):
        row_vals = set()
        col_vals = set()
        for j in range(9):
            if board[i][j] != 0:
                if board[i][j] in row_vals:
                    return False
                row_vals.add(board[i][j])

            if board[j][i] != 0:
                if board[j][i] in col_vals:
                    return False
                col_vals.add(board[j][i])

    for box_row in range(3):
        for box_col in range(3):
            seen = set()
            for i in range(3):
                for j in range(3):
                    num = board[box_row * 3 + i][box_col * 3 + j]
                    if num != 0:
                        if num in seen:
                            return False
                        seen.add(num)

    return True

class LlmSudokuSolver:
    def __init__(self, board):
        self.root = TreeNode(board)  # Root node
        self.current_node = self.root
        self.controller = ToTController()

    def find_empty_location(self, board):
        """Find an empty cell (0) in the board."""
        for i in range(9):
            for j in range(9):
                if board[i][j] == 0:
                    return i, j
        return None

    def prompt_llm(self, board):
        """Use LLM to suggest the next best move with a structured response."""
        prompt = f"""
        You are an expert Sudoku solver. Your task is to suggest a single valid move for the given Sudoku board.
        
        Sudoku Board:
        {board}

        Rules:
        - Format your response strictly as: `(row, col, num)`
        - Ensure the move follows Sudoku rules (no duplicates in row, column, or 3x3 box).
        - Do **not** provide explanations—only output a tuple in the exact format `(row, col, num)`.

        Example Response:
        ```
        (2, 3, 5)
        ```
        """
        response = llm.create_chat_completion(
            messages=[
                {"role": "system", "content": "You are a Sudoku-solving assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5  # Lower randomness for more structured output
        )

        return response["choices"][0]["message"]["content"].strip()


    def solve_with_tot(self, max_steps=100):
        """Main ToT-based solving loop with backtracking and LLM prompting."""
        for step in range(max_steps):
            print(f"\n🔹 Step {step+1} - Current Board State:")
            self.print_board(self.current_node.board)

            if is_valid_sudoku(self.current_node.board):
                print("✅ Board is valid. Checking for completion...")
                if not self.find_empty_location(self.current_node.board):
                    print("🎉 Sudoku solved!")
                    return self.current_node.board
            
            # Ask LLM for the best move
            move = self.prompt_llm(self.current_node.board)
            print(f"🔍 LLM Suggested Move: {move}")
            
            # Process LLM move
            new_board = self.apply_move(self.current_node.board, move)
            if new_board:
                new_node = self.current_node.add_child(new_board)
                self.current_node = new_node  # Move to the new state
            else:
                print("❌ LLM provided an invalid move, backtracking...")

            # Check if backtracking is needed
            if self.controller.should_backtrack(self.current_node):
                print("↩️ Backtracking triggered...")
                if self.current_node.parent:
                    self.current_node = self.current_node.parent  # Move back
                else:
                    print("🚨 No more parent nodes, stopping...")
                    return "Failed to solve"

        return "Failed to solve within step limit"


    def is_valid_move(self, board, row, col, num):
        """Check if placing 'num' at (row, col) is valid under Sudoku rules."""
        # Check row
        if num in board[row]:
            return False

        # Check column
        if num in [board[r][col] for r in range(9)]:
            return False

        # Check 3×3 box
        start_row, start_col = (row // 3) * 3, (col // 3) * 3
        for r in range(3):
            for c in range(3):
                if board[start_row + r][start_col + c] == num:
                    return False

        return True

    def apply_move(self, board, move):
        """Apply a move to the Sudoku board if it's valid."""
        try:
            match = re.search(r"\((\d+),\s*(\d+),\s*(\d+)\)", move)
            if not match:
                print(f"⚠️ Unable to parse move: {move}")
                return None
            
            row, col, num = map(int, match.groups())

            if board[row][col] != 0:
                print(f"❌ Invalid move: Cell ({row}, {col}) is already filled.")
                return None

            if not (1 <= num <= 9):
                print(f"❌ Invalid move: Number {num} is out of range.")
                return None

            if not self.is_valid_move(board, row, col, num):
                print(f"❌ Invalid move: {num} at ({row}, {col}) violates Sudoku rules.")
                return None

            new_board = copy.deepcopy(board)
            new_board[row][col] = num
            return new_board

        except Exception as e:
            print(f"⚠️ Error applying move: {e}")

        return None


    def print_board(self, board):
        """Display the Sudoku board."""
        for row in board:
            print(" ".join(str(cell) if cell != 0 else "*" for cell in row))



if __name__ == "__main__":
    import os
    import platform

    if platform.system() == "Windows":
        os.environ["ANSI_COLORS_DISABLED"] = "1"
    
    
    # Example usage
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

    solver = LlmSudokuSolver(board)
    solution = solver.solve_with_tot()
    print("\nFinal Solution:")
    solver.print_board(solution)